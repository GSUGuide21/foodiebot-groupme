import os
import re
import time

from manager import Group, GSpreadProvider

class FoodieBot:
	def __init__(self, app):
		self.name = "FoodieBot"
		self.token = os.environ.get("access_token", "")
		self.group_id = os.environ.get("group_id", "")
		self.bot_id = os.environ.get("bot_id", "")
		self.max_message_length = os.environ.get("max_message_length", 1000)
		self.prefix = os.environ.get("prefix", "$")
		self.current_group = Group(group_id=self.group_id).fetch() if self.group_id else None

	def dispatch(self):

		pass

	def reply(self, **message):
		pass

	def respond(self, **data):
		pass