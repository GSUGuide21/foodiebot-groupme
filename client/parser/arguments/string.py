from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from client.parser.arguments import ArgumentParseError


@dataclass(slots=True)
class StringArgument:
  name: str
  required: bool = True
  default: str | None = None
  greedy: bool = False

  def parse(self, arguments: Sequence[str], start_index: int) -> tuple[str | None, int]:
    if start_index >= len(arguments):
      if self.required and self.default is None:
        raise ArgumentParseError(f"Missing required argument: {self.name}")
      return self.default, start_index

    if self.greedy:
      return " ".join(arguments[start_index:]), len(arguments)

    return arguments[start_index], start_index + 1
