import os
from flask import Flask, request, jsonify
from threading import Thread
from client.client import Client

class ClientRuntime:
  def __init__(self):
    self.app = Flask(__name__)
    self.client = Client()

  def dispatch(self):
    print(
      os.environ.get("bot_id"),
      os.environ.get("group_id")
    )
    @self.app.post("/")
    def receive_message():
      data = request.get_json()
      print(data)
      if not data:
        return jsonify({"error": "Invalid request"}), 400

      try:
        Thread(target=self.client.reply, kwargs=data).start()
      except Exception as e:
        return jsonify({"error": str(e)}), 500

      return jsonify({"status": "Message received"}), 200
    
    self.client.dispatch()