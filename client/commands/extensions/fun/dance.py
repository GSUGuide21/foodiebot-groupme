from __future__ import annotations

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, IntArgument


DANCE_FRAMES = [
  "(>'-')> <('-'<) ^(' - ')^ v(' - ')v (>'-')>",
  "<(o_o<) <(o_o)> (>o_o)>",
  "_o/ _o_ \\o_",
]


class DanceCommand(Command):
  name = "dance"
  description = "Post a dance move"

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(
        IntArgument("index", required=False, default=1),
      )
    except ArgumentParseError:
      raise ValueError(f"Usage: {context.prefix}dance [1-{len(DANCE_FRAMES)}]")

    index = parsed["index"]
    if index is None or index < 1 or index > len(DANCE_FRAMES):
      raise ValueError(f"Usage: {context.prefix}dance [1-{len(DANCE_FRAMES)}]")

    return DANCE_FRAMES[index - 1]
