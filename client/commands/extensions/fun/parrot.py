from __future__ import annotations
from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, StringArgument

class Parrot(Command):
  name = "parrot"
  aliases = ["repeat"]
  description = "Parrot back what you say"

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(StringArgument("text", greedy=True))
    except ArgumentParseError:
      raise ValueError(f"Usage: {context.prefix}parrot <message>")

    text = parsed["text"]
    if text is None:
      raise ValueError(f"Usage: {context.prefix}parrot <message>")

    return text