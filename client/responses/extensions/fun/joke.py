from __future__ import annotations

import random
import re

from client.responses.base import Response


class JokeResponse(Response):
  name = "joke"
  description = "Tells a clean joke"
  priority = 5
  targets = [
    re.compile(r"^\s*(tell me a joke|joke|make me laugh|say a joke)\b[!.?\s]*$", re.IGNORECASE),
  ]

  _JOKES = [
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my calendar a joke, but it said its days were numbered.",
    "Why did the coffee file a police report? It got mugged.",
    "What do you call fake spaghetti? An impasta.",
  ]

  def execute(self, message, context):
    return random.choice(self._JOKES)
