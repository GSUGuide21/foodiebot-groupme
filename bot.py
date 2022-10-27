import os
import json
import requests
import re
import time
from threading import Thread
from importlib import reload

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from methods import commands, system, responses
from utils import Message, SenderType

app = Flask(__name__)
#db = SQLAlchemy(app)

BOT_ID = os.environ.get("bot_id", "")
APP_ID = os.environ.get("app_id", "")
PREFIX = os.environ.get("bot_prefix", "$")
API_URL = "https://api.groupme.com/v3/bots"

MAX_MESSAGE_LENGTH = 1000

"""
class Response(db.Model):
	__tablename__ = "responses"
	name = db.Column(db.String(64), primary_key=True)
	content = db.Column(db.String(256))
	image_url = db.Column(db.String(128))
"""

@app.route("/", methods=["POST"])
def receive():
	message = request.get_json()
	group_id = message["group_id"]

	Thread(target=reply, args=(message, group_id)).start()
	return "ok", 200

def reply(message, group_id):
	result = process(Message(message))
	send(result, group_id)

def process(message):
	bot_responses = []
	username = message.name

	print(f"Sender name: {username}")
	print(f"Sender type: {message.sender_type}")

	if message.sender_type == SenderType.User:
		if message.text.startswith(PREFIX):
			parts: list[str] = message.text[len(PREFIX):].strip().split(None, 1)
			command = parts.pop(0).lower()
			query = parts[0] if len(parts) > 0 else ""

			if PREFIX in command:
				pass
				
			elif command in commands:
				current_command = commands[command]
				if not current_command.has_args(query):
					bot_responses.append(current_command.ARGUMENT_WARNING)
				else:
					response = current_command.response(query, message, BOT_ID, APP_ID)
					if response != None:
						print(response)
						bot_responses.append(response)

			elif command == "help":
				if query:
					query = query.strip(PREFIX)
					if query in commands:
						description = commands[query]["description"]
						bot_responses.append(f"{PREFIX}{query}: {description}")
					else:
						bot_responses.append(f"The command ({command}) does not exist!")
				else:
					commands_info = [f"{PREFIX}{command}: {commands[command].DESCRIPTION}" for command in commands]
					result = """---Help---\n
					{}
					""".format("\n".join(commands_info))

					bot_responses.append(result)
		else:
			for key, value in responses.items():
				if value.REGEX and value.REGEX.match(message.text):
					matches = value.REGEX.findall(message.text)
					result = value.respond(message, matches)
					bot_responses.append(result)

	if message.sender_type == SenderType.System:
		for option in system:
			if system[option].REGEX.match(message.text):
				matches = system[option].REGEX.findall(message.text)
				bot_responses.append(system[option].response(message, matches))

	return bot_responses

def send(message, group_id):
	if isinstance(message, list):
		for item in message:
			send(item, group_id)
		return
	
	data = {
		"bot_id": BOT_ID
	}

	image = None
	if isinstance(message, tuple):
		message, image = message

	if message is None:
		message = ""

	if len(message) > MAX_MESSAGE_LENGTH:
		for block in [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]:
			send(block, group_id)
			time.sleep(0.3)
		
		data["text"] = ""
	else:
		data["text"] = message

	if image is not None:
		data["picture_url"] = image

	print("Issuing responses:")
	print(data)

	if data["text"] or data.get("picture_url"):
		response = requests.post(f"{API_URL}/post", json=data)

def sender_is_bot(message):
	return message['sender_type'] == "bot"