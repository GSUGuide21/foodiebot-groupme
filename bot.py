import os
import json
import requests
import re
from importlib import reload

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

from methods.index import methods

app = Flask(__name__)

with open(".secret", "r") as f:
	secrets = json.loads(f.read())
	bot_id = secrets["bot_id"]
	app_id = secrets["app_id"]

def handle(sender, message: str | None, bot_id, app_id):
	"""Route commands to the correct module function"""
	command = message.split()[0]
	result = methods.get(command)

	if isinstance(result, str):
		return result
	elif callable(result):
		return result(sender, message, bot_id, app_id)
	return None

@app.route('/', methods=['POST'])
def receive():
	"""Handles requests from GroupMe"""
	sender = request.get_json()["name"]
	message = request.get_json()["text"]

	print(message)

	if sender == "foodiebot":
		return "ok", 200
	
	if message and len(message) > 0 and message[0] == "$":
		result = handle(sender, message, bot_id, app_id)
		if result: reply(result)
	#elif 
	print(f'INCOMING REQUEST FROM {request.remote_addr}')
	return "ok", 200

def reply(message):
	"""Replies to a message in the chat"""
	url = 'https://api.groupme.com/v3/bots/post'
	
	if message == None or message == "None":
		return None
	
	data = { 
		'bot_id': bot_id,
		'text': message
	}

	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

	print(json)

def sender_is_bot(message):
	"""Checks if the sender is a bot to not reply to own messages"""
	return message['sender_type'] == "bot"