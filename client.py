import os
import re
import time
import requests

from beta.commands import commands
from beta.responses import responses
from beta.system import system
from beta.util import SenderType, RoleType
from beta.manager import Message, Group, Member, BotManager, Driver

class FoodieBot:
	def __init__(self):
		self.bot_id = os.environ.get("bot_id", "")
		self.app_id = os.environ.get("app_id", "")
		self.prefix = os.environ.get("prefix", "$")
		self.max_messages = os.environ.get("max_messages", 1000)
		self.access_token = os.environ.get("access_token")
		self.bot_manager = BotManager()
		self.driver = Driver()
		self.polls = []
		self.messages = []
		self.events = []
		self.state = {}

	def dispatch(self):
		group_id = os.environ.get("group_id", "")
		self.group_id = group_id if group_id != "" or group_id != None else ""
		self.group = Group(group_id=group_id) if self.group_id else None

		if self.group is None: return

		self.messages = self.group.get_messages()
		self.events = self.group.get_events()
		self.polls = self.group.get_polls()
		self.state = self.get_state()

		self.bot_manager.post({"text": "Hey, I'm FoodieBot! I'm going to be your friend today."})

	def get_state(self):
		return {}

	def reply(self, **message):
		group_id = message.get("group_id")
		if message is None or group_id == "": return None

		msg = Message(message)
		self.messages.append(msg)

		responses = []
		group = Group(group_id=group_id).fetch()
		sender = group.find_member(message.user_id)

		params = {}
		params["message"] = msg
		params["group"] = group
		params["client"] = self

		if msg.sender_type == SenderType.User:
			params["sender"] = sender
			response = self.parse_command(**params) if message.text.startswith(self.prefix) else self.parse_response(**params)
			responses.append(response)

		if msg.sender_type == SenderType.System:
			response = self.parse_system(**params)
			responses.append(response)

		if msg.sender_type == SenderType.Service:
			response = self.parse_service(**params)
			responses.append(response)

		responses = list(filter(lambda res: res != "" or res != None, responses))
		self.respond(reply=responses, group_id=group_id)

	def parse_command(self, **params):
		message: Message | None = params.get("message", None)
		sender: Member | None = params.get("sender", None)

		if message is None: return None

		parts = message.text[len(self.prefix):].strip().split(None)
		command = parts.pop(0).lower()
		query = str.join(" ", parts) if len(parts) > 0 else ""

		if self.prefix in command: return None

		options = {}
		options["message"] = message
		options["sender"] = sender
		options["command"] = command
		options["query"] = query

		return self.init_command(**options)

	def render_help(self, **options):
		command = options.get("command", "")
		info = {}

		if command != "" or command != None:
			if command in commands: return self.help_by_command(**options)
			for key, value in commands.items():
				has_aliases = isinstance(value.aliases, (list, tuple)) and len(value.aliases) > 0
				if not has_aliases: continue
				if command in value.aliases:
					options["command"] = key
					return self.help_by_command(**options)

		for key, cmd in commands.items():
			desc = cmd.description
			aliases = cmd.aliases or []
			category = cmd.category

			info[category] = info.get(category, [])

			opts = {}
			opts["description"] = desc
			opts["aliases"] = aliases
			opts["command"] = key

			result = self.render_help_item(**opts)
			info[category].append(result)

		response = []
		for category, cmds in info.items():
			cmd = "({category})\n{cmds}".format(category=category, commands=str.join("\n", cmds))
			response.append(cmd)

		return "---Help---\n{info}".format(info=str.join("\n", response))

	def help_by_command(self, **options):
		command = options.get("command")

		if command in commands:
			cmd = commands.get(command)
			desc = cmd.description
			aliases = cmd.aliases
			category = cmd.category

			opts = {}
			opts["description"] = desc
			opts["aliases"] = ""
			opts["category"] = ""
			opts["prefix"] = self.prefix
			opts["command"] = command

			has_aliases = isinstance(aliases, (list, tuple)) and len(aliases) > 0
			if has_aliases: opts["aliases"] = "\nAliases: {}".format(str.join(", ", aliases))
			if category != "": opts["category"] = "\nCategory: {}".format(category)
			return "{prefix}{command}: {description}{category}{aliases}".format(**opts)
		
		return "Command ({command}) is not available to you at this moment. Come back later".format(command=command)
		
	def render_help_item(self, **params):
		command = params.get("command")
		description = params.get("description")
		aliases = params.get("aliases")

		opts = {}
		opts["description"] = description
		opts["aliases"] = ""
		opts["command"] = command
		opts["prefix"] = self.prefix

		has_aliases = isinstance(aliases, (list, tuple)) and len(aliases) > 0
		if has_aliases: opts["aliases"] = " (aliases: {})".format(str.join(", ", aliases))
		return "{prefix}{command}: {description}{aliases}".format(**opts)

	def init_command(self, **options):
		command = options.get("command", "")
		query = options.get("query", "")
		
		if command == "": return ""

		if command == "help":
			query = query.strip(self.prefix).lower()
			if query != "": return self.render_help(command=query)
			return self.render_help()

		options["bot_id"] = self.bot_id
		options["app_id"] = self.app_id
		options["client"] = self

		if command in commands:
			target = commands.get(command, None)
			return self.dispatch_command(target, **options)

		for key, curr in commands.items():
			has_aliases = isinstance(curr.aliases, (list, tuple)) and len(curr.aliases) > 0
			if not has_aliases: continue
			if command in curr.aliases:
				options["command"] = key
				return self.init_command(**options)

		return "Command ({command}) is not available to you at this moment. Come back later".format(command=command)

	def dispatch_command(self, command, **options):
		query = options.get("query")
		preparsed = command.preparse(**options) if callable(command.preparse) else None

		options["query"] = preparsed if preparsed != None or preparsed != "" else query
		return command.run(**options)

	def parse_response(self, **options):
		for response in responses.values():
			valid = response.validate(**options)
			if valid: return response.respond(**options)

	def parse_system(self, **options):
		for response in system.values():
			valid = response.validate(**options)
			if valid: return response.respond(**options)

	def parse_service(self, **options):
		pass

	def respond(self, **data):
		reply = data.get("reply")
		group_id = data.get("group_id")

		if isinstance(reply, list):
			for item in reply: self.respond(reply=item, group_id=group_id)
			return

		if isinstance(reply, (dict, Message)):
			reply["bot_id"] = self.bot_id
			return self.respond_from_data(reply)

		params = {}
		params["bot_id"] = self.bot_id

		image = None

		if isinstance(reply, tuple): reply, image = reply
		if reply is None: reply = ""

		if len(reply) > self.max_messages:
			for block in [reply[i:i + self.max_messages] for i in range(0, len(reply), self.max_messages)]:
				self.respond(reply=block, group_id=group_id)
				time.sleep(0.3)

			params["text"] = ""

		else: params["text"] = reply

		if image != None: data["picture_url"] = image
		
		self.respond_from_data(params)

	def respond_from_data(self, data):
		if data["text"] or data.get("picture_url"):
			response = self.bot_manager.post(json=data)
			return response.json()["response"]
		else:
			return None