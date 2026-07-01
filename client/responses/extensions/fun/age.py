from __future__ import annotations
import re
from client.responses.base import Response

class AgeResponse(Response):
  name = "age"
  targets = [
    re.compile(r"\bhow old are you\b\??", re.IGNORECASE),
    re.compile(r"\bwhat is your age\b\??", re.IGNORECASE),
    re.compile(r"\bwhat's your age\b\??", re.IGNORECASE),
  ]
  description = "Responds with the bot's age"
  timeout_seconds = 2

  def execute(self, message, context):
    return "FoodieBot is 1 year old!"