import os, json, requests, re, time
from threading import Thread
from importlib import reload

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

from methods import commands, system, service, responses
from manager import Manager, Group, Member
from util import Message, SenderType

class FoodieBot(Manager):
	def __init__(self, **options):
		super().__init__(path="/bots")
		self.BOT_ID = options.get("bot_id", os.environ.get("bot_id", ""))
		self.APP_ID = options.get("app_id", os.environ.get("app_id", ""))
		self.PREFIX = options.get("bot_prefix", os.environ.get("bot_prefix", ""))
		self.MAX_MESSAGE_LENGTH = options.get("max_message_length", os.environ.get("max_message_length", ""))
		self.ACCESS_TOKEN = options.get("access_token", os.environ.get("access_token", ""))

	def reply(self, **options):
		message = options.get("message", "")
		group_id = options.get("group_id", "")

		result = self.process(message=message, group_id=group_id)
		self.send(result=result, group_id=group_id)

	def process(self, **options):
		pass

	def send(self, **options):
		pass

app = Flask(__name__)
client = FoodieBot(bot_prefix="$")

@app.route("/", methods=["POST"])
def receive():
	message = request.get_json()
	group_id = message["group_id"]

	Thread(target=client.reply, kwargs={"message": message, "group_id": group_id}).start()
	return "ok", 200