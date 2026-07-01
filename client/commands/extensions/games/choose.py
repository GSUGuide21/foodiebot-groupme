from __future__ import annotations

import random

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, StringArgument
from client.util import parse_csv_values

def choose_usage(prefix: str) -> str:
  return f"Usage: {prefix}choose <option1, option2, ...>"


class ChooseCommand(Command):
  name = "choose"
  aliases = ["pick"]
  description = "Pick an option"

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(StringArgument("options", greedy=True))
    except ArgumentParseError:
      return choose_usage(context.prefix)

    raw_options = parsed["options"]
    if not raw_options:
      return choose_usage(context.prefix)

    options = parse_csv_values(raw_options)
    if len(options) < 2:
      return choose_usage(context.prefix)

    return random.choice(options)
