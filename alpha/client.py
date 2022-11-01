import os, json, requests, re, time
from threading import Thread
from importlib import reload

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from methods import commands, system, responses
from utils import Message, SenderType

class FoodieBot:
	def __init__(self, **config):
		self.BOT_ID = os.environ.get("bot_id", config.bot_id)
		self.APP_ID = os.environ.get("app_id", config.app_id)
		self.PREFIX = os.environ.get("bot_prefix", config.bot_prefix)
		self.MAX_MESSAGE_LENGTH = os.environ.get("max_message_length", 1000)

		self.API_ENDPOINT = "https://api.groupme.com/v3/bots"
	
	def reply(self, message, group_id):
		result = self.process(Message(message))
		self.send(result, group_id)

	def process(self, message):
		bot_responses = []
		username = message.name

		print(f"Sender name: {username}")
		print(f"Sender type: {message.sender_type}")

		if message.sender_type == SenderType.User:
			if message.text.startswith(self.PREFIX):
				parts: list[str] = message.text[len(self.PREFIX):].strip().split(None, 1)
				command = parts.pop(0).lower()
				query = parts[0] if len(parts) > 0 else ""

				if self.PREFIX in command:
					pass
			
				response = self.init_command(
					message=message, command=command,
					query=query, username=username
				)

				if response != None:
					bot_responses.append(response)
			
			else:
				for key, response in responses.items():
					if response.REGEX and response.REGEX.match(message.text):
						matches = response.REGEX.findall(message.text)
						result = response.respond(message, matches)
						bot_responses.append(result)

		if message.sender_type == SenderType.System:
			for option in system:
				sys_cmd = system[option]
				if sys_cmd.REGEX and sys_cmd.REGEX.match(message.text):
					matches = sys_cmd.REGEX.findall(message.text)
					bot_responses.append(sys_cmd.respond(message, matches))

		return bot_responses

	def render_help(self):
		cmds_info = []

		for command in commands:
			cmd = commands[command]
			has_aliases = isinstance(cmd.ALIASES, list) and len(cmd.ALIASES) > 0
			aliases_str = ", ".join(cmd.ALIASES) if has_aliases else ""

			res = "{prefix}{command}: {description}{aliases}".format(
				prefix=self.PREFIX, command=command,
				description=cmd.DESCRIPTION,
				aliases=aliases_str
			)

			cmds_info.append(res)

		return "---Help---\n{info}".format(info="\n".join(cmds_info))

	def init_command(self, **options):
		message = options["message"]
		command = options["command"]
		query = options["query"]
		username = options["username"]

		if command == "help":
			if query:
				query = query.strip(self.PREFIX).lower()

				if query in commands:
					description = commands[query].DESCRIPTION
					aliases = commands[query].ALIASES

					aliases_str = "\nAliases: {result}".format(
						result=str.join(", ", aliases)
					) if isinstance(aliases, list) and len(aliases) > 0 else ""
					
					return "{prefix}{query}: {description}{aliases}".format(
						prefix=self.PREFIX, description=description,
						query=query, aliases=aliases_str
					)

				else:
					for key, cmd in commands:
						if isinstance(cmd.ALIASES, list) and len(cmd.ALIASES) > 0:
							if query in cmd.ALIASES:
								description = commands[key].DESCRIPTION
								aliases = commands[key].ALIASES

								aliases_str = "\nAliases: {result}".format(
									result=str.join(", ", aliases)
								) if isinstance(aliases, list) and len(aliases) > 0 else ""
					
								return "{prefix}{query}: {description}{aliases}".format(
									prefix=self.PREFIX, description=description,
									query=query, aliases=aliases_str
								)

					return f"The command ({query}) does not exist! Please view the available commands by using $help."													

			else:
				return self.render_help()
			
		elif command in commands:
			cmd = commands[command]
			if not cmd.has_args(query):
				return cmd.ARGUMENT_WARNING
			else:
				response = cmd.respond(query, message, self.BOT_ID, self.APP_ID)
				return response

	def send(self, message, group_id):
		if isinstance(message, list):
			for item in message:
				self.send(item, group_id)
			return

		data = {
			"bot_id": self.BOT_ID
		}

		image = None
		if isinstance(message, tuple):
			message, image = message

		if message is None:
			message = ""

		if len(message) > self.MAX_MESSAGE_LENGTH:
			for block in [message[i:i + self.MAX_MESSAGE_LENGTH] for i in range(0, len(message), self.MAX_MESSAGE_LENGTH)]:
				self.send(block, group_id)
				time.sleep(0.3)

			data["text"] = ""
		else:
			data["text"] = message

		if image is not None:
			data["picture_url"] = image
		
		print("Issuing responses:")
		print(data)

		if data["text"] or data.get("picture_url"):
			response = requests.post(f"{self.API_ENDPOINT}/post", json=data)

app = Flask(__name__)
client = FoodieBot()

@app.route("/", methods=["POST"])
def receive():
	message = request.get_json()
	group_id = message["group_id"]

	Thread(target=client.reply, args=(message, group_id)).start()
	return "ok", 200