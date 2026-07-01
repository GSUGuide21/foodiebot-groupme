from __future__ import annotations

from client.commands.base import Command
from client.manager import MeManager


ME_SNACKS = [
  "You are a burrito-powered coding machine.",
  "You are 67% coffee, 33% tacos.",
  "You are the chosen one of lunch planning.",
]


class MeCommand(Command):
  name = "me"
  description = "Playful status message"

  def execute(self, message, context):
    if context.token:
      profile = MeManager(token=context.token).get_profile()
      if isinstance(profile, dict):
        name = str(profile.get("name") or "").strip()
        user_id = str(profile.get("id") or profile.get("user_id") or "").strip()
        if name and user_id:
          return f"{name} (user_id={user_id})"
        if name:
          return name

    index = len(message.raw) % len(ME_SNACKS) if message.raw else 0
    return ME_SNACKS[index]
