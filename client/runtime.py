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
      "[startup] bot_id=",
      os.environ.get("bot_id"),
      "group_id=",
      os.environ.get("group_id")
    )

    @self.app.get("/health")
    def health_check():
      return jsonify({
        "status": "ok",
        "bot_configured": bool(os.environ.get("bot_id")),
        "group_configured": bool(os.environ.get("group_id")),
      }), 200

    @self.app.post("/")
    def receive_message():
      data = request.get_json()
      print("[webhook] payload received:", data)
      if not data:
        print("[webhook] invalid payload: empty or non-json body")
        return jsonify({"error": "Invalid request"}), 400

      try:
        Thread(target=self.client.reply, kwargs=data).start()
        print("[webhook] message dispatch scheduled")
      except Exception as e:
        print("[webhook] dispatch error:", str(e))
        return jsonify({"error": str(e)}), 500

      return jsonify({"status": "Message received"}), 200
    
    self.client.dispatch()