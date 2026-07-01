from __future__ import annotations

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, StringArgument

class YouTubeCommand(Command):
  name = "youtube"
  aliases = ["yt"]
  description = "Get a YouTube video link from a video source"

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(StringArgument("source", greedy=True))
    except ArgumentParseError:
      raise ValueError(f"Usage: {context.prefix}youtube <video source>")

    source = parsed["source"]
    if not source:
      raise ValueError(f"Usage: {context.prefix}youtube <video source>")

    return f"https://www.youtube.com/watch?v={source}"