from __future__ import annotations

import random as random_lib

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, IntArgument
from client.util import normalize_bounds, usage_error


class RandomCommand(Command):
  name = "random"
  aliases = ["rand"]
  description = "Generate a random integer in range"

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(
        IntArgument("start"),
        IntArgument("end"),
      )
    except ArgumentParseError:
      raise usage_error(context.prefix, "random", "<min> <max>")

    start = parsed["start"]
    end = parsed["end"]
    start, end = normalize_bounds(start, end)

    return str(random_lib.randint(start, end))
