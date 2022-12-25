from flask import Flask, request
from threading import Thread
from client import FoodieBot

app = Flask(__name__)
client = FoodieBot()

@app.post("/")
def receive():
	message = request.get_json()
	Thread(target=client.reply, kwargs=message)
	return "ok", 200

if __name__ == '__main__':
	client.dispatch()