from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

from client.parser.arguments import ArgumentParseError

@dataclass(slots=True)
class BoolArgument:
  name: str
  required: bool = True
  default: bool | None = None

  def parse(self, arguments: Sequence[str], start_index: int) -> tuple[bool | None, int]:
    if start_index >= len(arguments):
      if self.required and self.default is None:
        raise ArgumentParseError(f"Missing required argument: {self.name}")
      return self.default, start_index

    value_str = arguments[start_index].lower()
    if value_str in ("true", "1", "yes", "y"):
      return True, start_index + 1
    elif value_str in ("false", "0", "no", "n"):
      return False, start_index + 1
    else:
      raise ArgumentParseError(f"Invalid boolean value for argument '{self.name}': {arguments[start_index]}")