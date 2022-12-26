from flask import Flask, request
from threading import Thread
from client import FoodieBot

app = Flask(__name__)
client = FoodieBot()

@app.post("/")
def receive():
	message = request.get_json()
	Thread(target=client.reply, kwargs=message).start()
	return "ok", 200

client.dispatch()