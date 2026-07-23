import os
import json
from flask import Flask, request, jsonify
from threading import Thread
from client.client import Client

class ClientRuntime:
  def __init__(self):
    self.app = Flask(__name__)
    self.client = Client()

  def dispatch(self, send_init: bool = True):
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

    @self.app.route("/", methods=["POST"])
    def receive_message():
      data = self._read_webhook_payload()
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
    
    if send_init:
      self.client.dispatch()

  @staticmethod
  def _read_webhook_payload() -> dict | None:
    data = request.get_json(silent=True)
    print(data)
    if isinstance(data, dict):
      return data

    if request.form:
      form_data = request.form.to_dict(flat=True)
      if form_data:
        return form_data

    raw_body = request.get_data(as_text=True).strip()
    if not raw_body:
      return None

    try:
      parsed = json.loads(raw_body)
    except json.JSONDecodeError:
      return None

    return parsed if isinstance(parsed, dict) else None