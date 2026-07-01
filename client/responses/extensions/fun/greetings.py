from __future__ import annotations

import re

from client.responses.base import Response


class GreetingsResponse(Response):
  name = "greetings"
  description = "Responds to common greetings"
  priority = 5
  targets = [
    re.compile(r"^\s*(hi|hello|hey|yo|sup|good morning|good afternoon|good evening)\b[!.?\s]*$", re.IGNORECASE),
  ]

  def execute(self, message, context):
    return "Hey! Hope you're having a great day."
