from __future__ import annotations

import re

from client.responses.base import Response

class WelcomeResponse(Response):
  name = "welcome"
  description = "Responds to welcome phrases"
  priority = 5
  triggers = [
    "welcome back",
    "welcome home",
    "welcome aboard",
    "welcome",
  ]

  def execute(self, message, context):
    return "Welcome! Glad you're here."
