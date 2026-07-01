from __future__ import annotations

import builtins
from dataclasses import dataclass
from typing import Any, Protocol, Sequence


class ArgumentParseError(ValueError):
  def __init__(self, message: str):
    super().__init__(f"ArgumentParseError: {message}")


class ArgumentSpec(Protocol):
  name: str

  def parse(self, arguments: Sequence[str], start_index: int) -> tuple[Any, int]:
    ...

@dataclass(slots=True)
class ParsedArguments:
  values: dict[str, Any]
  remaining: list[str]

  def __getitem__(self, key: str) -> Any:
    return self.values[key]

class Args:
  def __init__(self, arguments: Sequence[str]):
    self._arguments = builtins.list(arguments)
    self._index = 0

  def __iter__(self):
    return self

  def __next__(self):
    if self._index >= len(self._arguments):
      raise StopIteration
    value = self._arguments[self._index]
    self._index += 1
    return value

  def take(self):
    if self._index >= len(self._arguments):
      raise IndexError("No more arguments to take")
    value = self._arguments[self._index]
    self._index += 1
    return value

  def peek(self):
    if self._index >= len(self._arguments):
      return None
    return self._arguments[self._index]

  def has_next(self):
    return self._index < len(self._arguments)

  def parse(self, *specs: ArgumentSpec, allow_extra: bool = False) -> ParsedArguments:
    parsed: dict[str, Any] = {}
    index = self._index

    for spec in specs:
      value, index = spec.parse(self._arguments, index)
      parsed[spec.name] = value

    remaining = builtins.list(self._arguments[index:])
    if remaining and not allow_extra:
      raise ArgumentParseError(f"Unexpected arguments: {remaining}")

    self._index = index
    return ParsedArguments(values=parsed, remaining=remaining)

from client.parser.arguments.number import NumberArgument
from client.parser.arguments.list import ListArgument
from client.parser.arguments.string import StringArgument
from client.parser.arguments.bool import BoolArgument
from client.parser.arguments.float import FloatArgument
from client.parser.arguments.int import IntArgument

def parse_arguments(arguments: Sequence[str], *specs: ArgumentSpec, allow_extra: bool = False) -> ParsedArguments:
  args = Args(arguments)
  return args.parse(*specs, allow_extra=allow_extra)

__all__ = [
  "Args",
  "ArgumentParseError",
  "ArgumentSpec",
  "ListArgument",
  "ParsedArguments",
  "StringArgument",
  "NumberArgument",
  "BoolArgument",
  "FloatArgument",
  "IntArgument",
  "parse_arguments"
]
