from __future__ import annotations

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, StringArgument, parse_arguments


HERE_WE_GO_PREFIX = "Here we go:"

class HereWeGoCommand(Command):
  name = "herewego"
  aliases = ["hwg"]
  description = "Announce a message with hype"

  def execute(self, message, context):
    try:
      parsed = parse_arguments(message.positional_arguments, StringArgument("text", greedy=True))
    except ArgumentParseError:
      raise ValueError(f"Usage: {context.prefix}herewego <message>")

    text = str(parsed["text"] or "").strip()
    if not text:
      raise ValueError(f"Usage: {context.prefix}herewego <message>")

    reply_text = f"{HERE_WE_GO_PREFIX} {text}"
    image_url = str(
      message.keyword_arguments.get("image_url")
      or message.keyword_arguments.get("image")
      or ""
    ).strip()

    if image_url:
      return {
        "text": reply_text,
        "attachments": [
          {
            "type": "image",
            "url": image_url,
          }
        ],
      }

    return reply_text