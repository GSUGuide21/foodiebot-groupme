from __future__ import annotations

import random

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, IntArgument
from client.util import format_usage, parse_int

def roll_result(count: int, sides: int, values: list[int]) -> str:
  return f"roll: {count}d{sides} -> {values} (total={sum(values)})"

class RollCommand(Command):
  name = "roll"
  description = "Roll dice (default 1d6)"
  timeout_seconds = 2

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(
        IntArgument("count", required=False, default=1),
        IntArgument("sides", required=False, default=6),
        allow_extra=True,
      )
    except ArgumentParseError as exc:
      raise ValueError(str(exc)) from exc

    if parsed.remaining:
      raise ValueError(
        f"{format_usage(context.prefix, 'roll', '[count] [sides]')} | "
        f"{format_usage(context.prefix, 'roll', 'count=<n> sides=<n>')}"
      )

    count = parsed["count"]
    sides = parsed["sides"]

    keyword_count = message.keyword_arguments.get("count")
    keyword_sides = message.keyword_arguments.get("sides")

    if keyword_count is not None:
      count = parse_int("count", keyword_count)
    if keyword_sides is not None:
      sides = parse_int("sides", keyword_sides)

    count = parse_int("count", count, minimum=1, maximum=50)
    sides = parse_int("sides", sides, minimum=2, maximum=1000)

    values = [random.randint(1, sides) for _ in range(count)]
    return roll_result(count=count, sides=sides, values=values)
