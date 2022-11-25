import json
import os
import re
import time
from importlib import reload
from threading import Thread
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from methods import commands, responses, service, system
from util import Message, SenderType
from manager import Group, Manager, Member

class FoodieBot(Manager):
	def __init__(self, **config):
		super(FoodieBot, self).__init__(path="bots")

		self.bot_id = config.get("bot_id", os.environ.get("bot_id", ""))
		self.app_id = config.get("app_id", os.environ.get("app_id", ""))
		self.prefix = config.get("prefix", os.environ.get("prefix", ""))
		self.max_message_length = config.get("max_message_length", os.environ.get("max_message_length", ""))
		self.access_token = config.get("access_token", os.environ.get("access_token", ""))

	def reply(self, **message):
		print(message)
		print(self.url)

		responses = []
		group_id = message.get("group_id")

		if message is None or group_id == "": return None

		message = Message(message)
		group = Group(group_id=group_id).fetch()
		sender = group.find_member(message.user_id)

		params = {
			"message": message,
			"group": group,
			"client": self
		}

		if message.sender_type == SenderType.User:
			params["sender"] = sender
			if message.text.startswith(self.prefix):
				print(message)

	def respond(self, **data):
		message = data.get("result")
		group_id = data.get("group_id")

		if isinstance(message, list):
			for item in message: self.respond(result=item, group_id=group_id)
			return

		if isinstance(message, (dict, Message)):
			message["bot_id"] = self.bot_id
			return self.respond_from_data(message)

		params = { "bot_id": self.bot_id }
		image = None

		if isinstance(message, tuple):
			message, image = message

		if message is None: message = ""

		if len(message) > self.max_message_length:
			for block in [message[i:i + self.max_message_length] for i in range(0, len(message), self.max_message_length)]:
				self.respond(result=block, group_id=group_id)
				time.sleep(0.3)

			params["text"] = ""

		else: params["text"] = message

		if image != None: data["picture_url"] = image

		self.respond_from_data(params)

	def respond_from_data(self, params):
		if params["text"] or params.get("picture_url"):
			response = requests.post(f"{self.url}/post", json=params)
"""		
class FoodieBot(Manager):
	def __init__(self, **config):
		super(FoodieBot, self).__init__(path="bots")

		self.bot_id = config.get("bot_id", os.environ.get("bot_id", ""))
		self.app_id = config.get("app_id", os.environ.get("app_id", ""))
		self.prefix = config.get("prefix", os.environ.get("prefix", ""))
		self.max_message_length = config.get("max_message_length", os.environ.get("max_message_length", ""))
		self.access_token = config.get("access_token", os.environ.get("access_token", ""))

	def reply(self, **options):
		message = options.get("message", "")
		group_id = options.get("group_id", "")
		self.send(message=message, group_id=group_id)

	def send(self, **options):
		message = options.get("message", "")
		group_id = options.get("group_id", "")

		if message == "" or group_id == "":
			return None

		responses = []
		message = Message(message)
		group = Group(group_id=group_id).fetch()
		sender = group.find_member(message.user_id)

		params = {
			"message": message,
			"group": group,
			"client": self
		}

		if message.sender_type == SenderType.User:
			params["sender"] = sender
			if message.text.startswith(self.prefix):
				response = self.parse_command(**params)
				if response != None: responses.append(response)
			else: 
				response = self.parse_response(**params)
				if response != None: responses.append(response)

		if message.sender_type == SenderType.System:
			params["sender"] = None
			response = self.parse_system(**params)
			if response != None: responses.append(response)

		if message.sender_type == SenderType.Service:
			pass

		self.respond(result=responses, group_id=group_id)
	
	def parse_command(self, **options):
		message = options.get("message", None)
		sender = options.get("sender", None)

		if message is None: return None

		parts = message.text[len(self.prefix):].strip().split(None, 1)
		command = parts.pop(0).lower()
		query = parts[0] if len(parts) > 0 else ""

		if self.prefix in command: return None

		params = {
			"message": message,
			"sender": sender,
			"command": command,
			"query": query,
			"bot_id": self.bot_id,
			"app_id": self.app_id,
			"client": self
		}

		return self.init_command(**params)

	def init_command(self, **params):
		command = params.get("command")

		if command == "": return ""
		query = params.get("query", "")

		if command == "help":
			if query != "":
				query = query.strip(self.prefix).lower()
				return self.render_help(command=query)

			else: return self.render_help()
		
		if command in commands:
			curr = commands[command]
			return curr.respond(**params)
		
		sender: Member = params.get("sender")
		message = params.get("message")
		bot_id = params.get("bot_id")
		app_id = params.get("app_id")
		
		opts = {
			"message": message,
			"query": query,
			"bot_id": bot_id,
			"app_id": app_id,
			"sender": sender,
			"client": self
		}

		for key, curr in commands.items():
			if isinstance(curr.ALIASES, list) and len(curr.ALIASES) > 0:
				if command in curr.ALIASES: 
					opts["command"] = key
					return self.init_command(**opts)

		return "Command ({command}) is not available to you at this moment. Come back later".format(command=command)

	def render_help(self, **params):
		command = params.get("command", "")

		if command != "": return self.render_help_by_command(command)

		info = {}

		for key, command in commands.items():
			desc = command.DESCRIPTION
			aliases = command.ALIASES or []
			category = command.CATEGORY

			info[category] = info.get(category, [])

			opts = { "description": desc, "aliases": aliases, "command": key }
			result = self.render_help_item(**opts)

			info[category].append(result)

		response = []

		for category, cmds in info.items():
			cmd = "({category})\n{cmds}".format(category=category, commands=str.join("\n", cmds))
			response.append(cmd)

		return "---Help---\n{info}".format(info=str.join("\n", response))

	def render_help_by_command(self, command):
		if command in commands:
			curr = commands[command]
			desc = curr.DESCRIPTION
			aliases = curr.ALIASES
			category = curr.CATEGORY

			opts = { 
				"description": desc, 
				"aliases": "", 
				"category": "", 
				"prefix": self.prefix,
				"command": command
			}

			if isinstance(aliases, list) and len(aliases) > 0:
				aliases_s = str.join(", ", aliases)
				opts["aliases"] = "\nAliases: {aliases}".format(aliases=aliases_s)

			if category != "":
				opts["category"] = "\nCategory: {category}".format(category=category)

			return "{prefix}{command}: {description}{category}{aliases}".format(**opts)
		else:
			for key, curr in commands.items():
				if isinstance(curr.ALIASES, list) and len(curr.ALIASES) > 0:
					if command in curr.ALIASES:
						return self.render_help_by_command(key)

		return f"The command ({command}) does not exist! Please view the available commands by using $help."

	def parse_response(self, **options):
		for response in responses.values():
			if callable(response.validate) and response.validate(**options):
				return response.respond(**options)

	def parse_system(self, **options):
		for sys_cmd in system.values():
			if callable(sys_cmd.validate) and sys_cmd.validate(**options):
				return sys_cmd.respond(**options)

	def parse_service(self, **options):
		pass

	def render_help_item(self, **params):
		command = params.get("command")
		description = params.get("description")
		aliases = params.get("aliases")

		opts = {
			"description": description,
			"command": command,
			"prefix": self.prefix,
			"aliases": ""
		}

		if isinstance(aliases, list) and len(aliases) > 0:
			result = str.join(", ", aliases)
			opts["aliases"] = " (aliases: {result})".format(result=result)

		return "{prefix}{command}: {description}{aliases}".format(**opts)

	def respond(self, **options):
		message = options.get("result")
		group_id = options.get("group_id")

		if isinstance(message, list):
			for item in message:
				self.respond(result=item, group_id=group_id)
			return

		if isinstance(message, (dict, Message)):
			message["bot_id"] = self.bot_id
			return self.respond_from_data(data=message, group_id=group_id)

		data = {
			"bot_id": self.bot_id
		}

		image = None

		if isinstance(message, tuple):
			message, image = message

		if message is None:
			message = ""

		if len(message) > self.max_message_length:
			for block in [message[i:i + self.max_message_length] for i in range(0, len(message), self.max_message_length)]:
				self.send(result=block, group_id=group_id)
				time.sleep(0.3)

			data["text"] = ""
		
		else: data["text"] = message

		if image != None: data["picture_url"] = image

		self.respond_from_data(data)

	def respond_from_data(self, data):
		if data["text"] or data.get("picture_url"):
			response = requests.post(f"{self.url}/post", json=data)
"""

app = Flask(__name__)
client = FoodieBot(bot_prefix="$")

@app.route("/", methods=["POST"])
def receive():
	message = request.get_json()
	Thread(target=client.reply, kwargs=message).start()
	return "ok", 200

"""
from methods import commands, system, responses
from util import Message, SenderType, Group, Member

class FoodieBot:
	def __init__(self, **config):
		self.BOT_ID = config.get("bot_id", os.environ.get("bot_id", ""))
		self.APP_ID = config.get("app_id", os.environ.get("app_id", ""))
		self.PREFIX = config.get("bot_prefix", os.environ.get("bot_prefix", ""))
		self.MAX_MESSAGE_LENGTH = config.get("max_message_length", os.environ.get("max_message_length", 1000))
		self.ACCESS_TOKEN = config.get("access_token", os.environ.get("access_token", ""))

		self.BOT_ENDPOINT = "https://api.groupme.com/v3/bots"
		self.GROUPS_ENDPOINT = "https://api.groupme.com/v3/groups"

	def reply(self, message, group_id):
		result = self.process(message=message, group_id=group_id)
		self.send(result=result, group_id=group_id)

	def process(self, **options):
		responses = []
		message = options.get("message", "")
		group_id = options.get("group_id", None)

		if message == "" or group_id == "":
			return responses

		message = Message(message)
		group = Group(group_id).fetch()
		sender = group.find_member(message.user_id)

		print(f"Sender: {sender.nick} ({sender.id})")

		if message.sender_type == SenderType.User:
			if message.text.startswith(self.PREFIX):
				response = self.parse_command(
					message=message, 
					sender=sender,
					group=group,
					client=self
				)
				if response != None:
					responses.append(response)
			else:
				response = self.parse_response(
					message=message,
					sender=sender,
					group=group,
					client=self
				)
				if response != None:
					responses.append(response)

		if message.sender_type == SenderType.System:
			response = self.parse_sys(
				message=message,
				group=group,
				client=self
			)
			if response != None:
				responses.append(response)

		if message.sender_type == SenderType.Service:
			pass

		return responses

	def parse_command(self, **options):
		message = options.get("message", None)
		sender = options.get("sender", None)
		
		if message is None:
			return None
		
		parts = message.text[len(self.PREFIX):].strip().split(None, 1)
		command = parts.pop(0).lower()
		query = parts[0] if len(parts) > 0 else ""

		if self.PREFIX in command:
			return None

		return self.init_command(
			message=message,
			command=command,
			query=query,
			bot_id=self.BOT_ID,
			app_id=self.APP_ID,
			sender=sender,
			client=self
		)

	def init_command(self, **options):
		command = options.get("command")
		query = options.get("query", "")
		sender: Member = options.get("sender")
		message = options.get("message")
		bot_id = options.get("bot_id")
		app_id = options.get("app_id")

		if command == "":
			return ""

		if command == "help":
			if query:
				query = query.strip(self.PREFIX).lower()
				return self.render_help_by_command(command=query)
			else:
				return self.render_help()

		if command in commands:
			cmd = commands[command]
			response = cmd.respond(**options)
			return response

		for key, cmd in commands.items():
			if isinstance(cmd.ALIASES, list) and len(cmd.ALIASES) > 0:
				if command in cmd.ALIASES:
					return self.init_command(
						command=key,
						message=message,
						query=query,
						bot_id=bot_id,
						app_id=app_id,
						sender=sender,
						client=self
					)

		return "Command ({command}) is not available to you at this moment. Come back later".format(command=command)

	def render_help(self):
		cmds_info: dict[str, list] = {}

		for key, command in commands.items():
			description = command.DESCRIPTION
			aliases = command.ALIASES
			category = command.CATEGORY

			cmds_info[category] = cmds_info.get(category, [])

			result = self.render_help_item(
				description=description, 
				aliases=aliases,
				command=key
			)

			cmds_info[category].append(result)

		response = []
		for category, commands in cmds_info.items():
			cmd_str = ":{category}:\n{commands}".format(
				category=category,
				commands="\n".join(commands)
			)
			response.append(cmd_str)

		return "---Help---\n{info}".format(info="\n".join(response))

	def render_help_item(self, **options):
		command = options.get('command')
		description = options.get('description')
		aliases = options.get('aliases')

		aliases_l = str.join(", ", aliases) if isinstance(aliases, list) and len(aliases) > 0 else ""
		aliases_s = "(aliases: {result})".format(result=aliases_l) if aliases_l != "" else ""

		return "{prefix}{command}: {description} {aliases}".format(
			prefix=self.PREFIX,
			description=description,
			aliases=aliases_s,
			command=command			
		)

	def render_help_by_command(self, **options):
		command = options.get("command")

		if command in commands:
			description = commands[command].DESCRIPTION
			aliases = commands[command].ALIASES
			category = commands[command].CATEGORY

			aliases_l = str.join(", ", aliases) if isinstance(aliases, list) and len(aliases) > 0 else ""
			aliases_s = "\nAliases: {result}".format(result=aliases_l) if aliases_l != "" else ""

			category_s = "\nCategory: {category}".format(category=category) if category != "" else ""

			return "{prefix}{command}: {description}{category}{aliases}".format(
				prefix=self.PREFIX,
				description=description,
				command=command,
				aliases=aliases_s,
				category=category_s
			)
		else:
			for key, cmd in commands.items():
				if isinstance(cmd.ALIASES, list) and len(cmd.ALIASES) > 0:
					if command in cmd.ALIASES:
						return self.render_help_by_command(command=key)

		return f"The command ({command}) does not exist! Please view the available commands by using $help."

	def parse_response(self, **options):
		for response in responses.values():
			if callable(response.validate) and response.validate(**options):
				return response.respond(**options)


	def parse_sys(self, **options):
		for sys_cmd in system.values():
			if callable(sys_cmd.validate) and sys_cmd.validate(**options):
				return sys_cmd.respond(**options)

	def remove(self, **options):
		sender: Member | None = options.get("sender")
		group: Group = options.get("group")
		
		if sender is None:
			return False

		members_url = f"{self.GROUPS_ENDPOINT}/{group.group_id}/members"
		url = f"{members_url}/{sender.id}/remove"

		headers = {
			"X-Access-Token": self.ACCESS_TOKEN
		}

		response = requests.post(url, headers=headers)

	def send(self, **options):
		message = options.get("result")
		group_id = options.get("group_id")

		if isinstance(message, list):
			for item in message:
				self.send(result=item, group_id=group_id)
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
				self.send(result=block, group_id=group_id)
				time.sleep(0.3)

			data["text"] = ""
		else:
			data["text"] = message

		if image != None:
			data["picture_url"] = image

		print("Issuing responses:")
		print(data)

		if data["text"] or data.get("picture_url"):
			response = requests.post(f"{self.BOT_ENDPOINT}/post", json=data)


app = Flask(__name__)
client = FoodieBot(bot_prefix="$")

@app.route("/", methods=["POST"])
def receive():
	message = request.get_json()
	group_id = message["group_id"]

	Thread(target=client.reply, args=(message, group_id)).start()
	return "ok", 200
"""