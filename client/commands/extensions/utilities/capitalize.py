from __future__ import annotations

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, StringArgument

class CapitalizeCommand(Command):
  name = "capitalize"
  aliases = ["cap"]
  description = "Capitalize the first letter of each word"

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(StringArgument("text", greedy=True))
    except ArgumentParseError:
      raise ValueError(f"Usage: {context.prefix}capitalize <message>")

    text = parsed["text"]
    if text is None:
      raise ValueError(f"Usage: {context.prefix}capitalize <message>")

    return text.title()