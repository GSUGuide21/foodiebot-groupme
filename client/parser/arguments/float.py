from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

from client.parser.arguments import ArgumentParseError

@dataclass(slots=True)
class FloatArgument:
  name: str
  required: bool = True
  default: float | None = None

  def parse(self, arguments: Sequence[str], start_index: int) -> tuple[float | None, int]:
    if start_index >= len(arguments):
      if self.required and self.default is None:
        raise ArgumentParseError(f"Missing required argument: {self.name}")
      return self.default, start_index

    try:
      value = float(arguments[start_index])
    except ValueError:
      raise ArgumentParseError(f"Invalid float value for argument '{self.name}': {arguments[start_index]}")

    return value, start_index + 1