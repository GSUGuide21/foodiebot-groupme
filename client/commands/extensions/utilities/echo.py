from __future__ import annotations

from client.commands.base import Command

def echo_usage(prefix: str) -> str:
  return f"Usage: {prefix}echo <text>"

class EchoCommand(Command):
  name = "echo"
  aliases = ["say"]
  description = "Repeat text"

  def execute(self, message, context):
    if not message.arguments:
      return echo_usage(context.prefix)
    return message.arg_text
