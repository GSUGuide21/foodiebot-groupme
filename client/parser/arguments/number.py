from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

from client.parser.arguments import ArgumentParseError

@dataclass(slots=True)
class NumberArgument:
  name: str
  required: bool = True
  default: float | int | None = None

  def parse(self, arguments: Sequence[str], start_index: int) -> tuple[float | int | None, int]:
    if start_index >= len(arguments):
      if self.required and self.default is None:
        raise ArgumentParseError(f"Missing required argument: {self.name}")
      return self.default, start_index

    token = arguments[start_index]
    try:
      int_value: int = int(token)
      float_value: float = float(token)

      if int_value == float_value:
        value = int_value
      else:
        value = float_value
    except ValueError:
      raise ArgumentParseError(
        f"Invalid number value for argument '{self.name}': {token}"
      )

    return value, start_index + 1