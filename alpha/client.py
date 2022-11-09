import os, json, requests, re, time
from threading import Thread
from importlib import reload

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from methods import commands, system, responses
from util import Message, SenderType, Group

class FoodieBot:
	def __init__(self, **config):
		self.BOT_ID = os.environ.get("bot_id", config.get("bot_id", ""))
		self.APP_ID = os.environ.get("app_id", config.get("app_id", ""))
		self.PREFIX = os.environ.get("bot_prefix", config.get("bot_prefix", ""))
		self.ACCESS_TOKEN = os.environ.get("access_token", config.get("access_token", ""))
		self.MAX_MESSAGE_LENGTH = os.environ.get("max_message_length", 1000)

		self.BOT_ENDPOINT = "https://api.groupme.com/v3/bots"
		self.GROUPS_ENDPOINT = "https://api.groupme.com/v3/groups"

	def reply(self, message, group_id):
		result = self.process_message(message, group_id)
		self.send(result, group_id)

	def process_message(self, message, group_id):
		bot_responses = []
		message = Message(message)
		username = message.name
		group = Group(group_id).fetch()

		if message.sender_type == SenderType.User:
			if message.text.startswith(self.PREFIX):
				parts = message.text[len(self.PREFIX):].strip().split(None,1)
				command = parts.pop(0).lower()
				query = parts[0] if len(parts) > 0 else ""

				if self.PREFIX in command:
					pass

				response = self.init_command(
					message=message,
					command=command,
					query=query,
					username=username,
					group=group,
					bot_id=self.BOT_ID,
					app_id=self.APP_ID,
					client=self,				
				)

				if response != None:
					bot_responses.append(response)
			
			else:
				for response in responses.values():
					if response.REGEX and response.REGEX.match(message.text):
						matches = response.REGEX.findall(message.text)
						result = response.respond(
							message=message,
							group=group,
							matches=matches,
							client=self
						)
						bot_responses.append(result)

		if message.sender_type == SenderType.System:
			for sys_cmd in system.values():
				if sys_cmd.REGEX and sys_cmd.REGEX.match(message.text):
					matches = sys_cmd.REGEX.findall(message.text)
					result = response.respond(
						message=message,
						group=group,
						matches=matches,
						client=self
					)
					bot_responses.append(result)

		return bot_responses

	def render_help(self):
		cmds_info: dict[str,list[str]] = {}

		for command in commands:
			cmd = commands[command]
			category = cmd.CATEGORY or "Other"

			if category and not cmds_info[category]:
				cmds_info[category] = []
			
			has_aliases = isinstance(cmd.ALIASES, list) and len(cmd.ALIASES) > 0
			aliases_str = ", ".join(cmd.ALIASES) if has_aliases else ""

			result = "{prefix}{command}: {description}{aliases}".format(
				prefix=self.PREFIX, command=command,
				description=cmd.DESCRIPTION,
				aliases=aliases_str
			)

			cmds_info[category].append(result)

		cmds_info_w_cat = []
		for category, cmds in cmds_info.items():
			result = "-{category}-:\n{cmds}".format(
				category=category
				cmds=str.join("\n", cmds)
			)
			cmds_info_w_cat.append(result)

		return "---Help---\n{info}".format(info="\n".join(cmds_info_w_cat))
	
	def init_command(self, **options):
		command = options["command"]
		query = options.get("query", "")

		if command == "":
			return ""

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
					for key, cmd in commands.items():
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
			if callable(cmd.precondition) and cmd.precondition(**options):
				return cmd.PRECONDITION_WARNING
			else:
				response = cmd.respond(**options)
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

	def remove(self, **options):
		group = options.get("group", None)
		
		if group is None:
			return False
		
		target = options.get()