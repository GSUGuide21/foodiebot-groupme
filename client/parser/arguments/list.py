from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from client.parser.arguments import ArgumentParseError

@dataclass(slots=True)
class ListArgument:
  name: str
  required: bool = False
  min_length: int = 0
  default: list[str] = field(default_factory=list)

  def parse(self, arguments: Sequence[str], start_index: int) -> tuple[list[str], int]:
    values = list(arguments[start_index:])

    if not values:
      if self.required or self.min_length > 0:
        raise ArgumentParseError(f"Missing required argument list: {self.name}")
      return list(self.default), start_index

    if len(values) < self.min_length:
      raise ArgumentParseError(
        f"Argument list '{self.name}' requires at least {self.min_length} values"
      )

    return values, len(arguments)
