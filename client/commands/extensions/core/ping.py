from __future__ import annotations

from client.commands.base import Command

def pong_message() -> str:
  return "pong"

class PingCommand(Command):
  name = "ping"
  description = "Health check"

  def execute(self, message, context):
    return pong_message()
