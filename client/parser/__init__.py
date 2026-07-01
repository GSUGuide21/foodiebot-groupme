from __future__ import annotations
from dataclasses import dataclass, field
import shlex
import re

from client.parser.arguments import ParsedArguments, parse_arguments


_FLAG_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_\-]*$")

@dataclass(slots=True)
class ParsedMessage:
  raw: str
  command: str = ""
  arguments: list[str] = field(default_factory=list)
  positional_arguments: list[str] = field(default_factory=list)
  keyword_arguments: dict[str, str] = field(default_factory=dict)
  keyword_arguments_all: dict[str, list[str]] = field(default_factory=dict)
  flags: set[str] = field(default_factory=set)
  warnings: list[str] = field(default_factory=list)

  @property
  def arg_text(self) -> str:
    return " ".join(self.arguments)

  def __bool__(self) -> bool:
    return bool(self.command)

  def __repr__(self) -> str:
    return (
      "ParsedMessage(" 
      f"raw={self.raw!r}, "
      f"command={self.command!r}, "
      f"arguments={self.arguments!r}, "
      f"positional_arguments={self.positional_arguments!r}, "
      f"keyword_arguments={self.keyword_arguments!r}, "
      f"keyword_arguments_all={self.keyword_arguments_all!r}, "
      f"flags={self.flags!r}, "
      f"warnings={self.warnings!r}"
      ")"
    )

  def parse_arguments(self, *specs, allow_extra: bool = False) -> ParsedArguments:
    return parse_arguments(self.arguments, *specs, allow_extra=allow_extra)

  def get_keywords(self, key: str) -> list[str]:
    return list(self.keyword_arguments_all.get(key.strip().lower(), []))

  def has_flag(self, name: str) -> bool:
    return name.strip().lower() in self.flags

class Parser:
  def __init__(self, prefix: str = "$"):
    self.prefix = prefix

  def split_tokens(self, text: str) -> tuple[list[str], str | None]:
    try:
      return shlex.split(text), None
    except ValueError:
      # Preserve legacy fallback behavior, but surface a warning so callers can react.
      return text.split(), "Could not parse quotes cleanly; parsed using basic whitespace splitting."

  def set_prefix(self, prefix: str) -> None:
    self.prefix = prefix

  def split_argument_styles(self, arguments: list[str]) -> tuple[list[str], dict[str, str], dict[str, list[str]], set[str]]:
    positional: list[str] = []
    keyword: dict[str, str] = {}
    keyword_all: dict[str, list[str]] = {}
    flags: set[str] = set()

    for token in arguments:
      if token.startswith("--") and len(token) > 2:
        raw_flag = token[2:].strip().lower()
        if raw_flag.startswith("no-"):
          flag = raw_flag[3:]
          if _FLAG_PATTERN.match(flag):
            keyword[flag] = "false"
            keyword_all.setdefault(flag, []).append("false")
            continue
        if _FLAG_PATTERN.match(raw_flag):
          flags.add(raw_flag)
          keyword[raw_flag] = "true"
          keyword_all.setdefault(raw_flag, []).append("true")
          continue

      if "=" not in token or token.startswith("="):
        positional.append(token)
        continue

      key, value = token.split("=", 1)
      normalized_key = key.strip().lower()
      if not normalized_key:
        positional.append(token)
        continue

      keyword[normalized_key] = value
      keyword_all.setdefault(normalized_key, []).append(value)

    return positional, keyword, keyword_all, flags

  def parse(self, text: str | None) -> ParsedMessage:
    normalized = (text or "").strip()

    if not normalized or not self.prefix or not normalized.startswith(self.prefix):
      return ParsedMessage(raw=normalized)

    command_text = normalized[len(self.prefix):].strip()
    if not command_text:
      return ParsedMessage(raw=normalized)

    tokens, token_warning = self.split_tokens(command_text)
    if not tokens:
      return ParsedMessage(raw=normalized)

    command_name = tokens[0].lower()
    arguments = tokens[1:]
    positional_arguments, keyword_arguments, keyword_arguments_all, flags = self.split_argument_styles(arguments)

    warnings: list[str] = []
    if token_warning:
      warnings.append(token_warning)

    return ParsedMessage(
      raw=normalized,
      command=command_name,
      arguments=arguments,
      positional_arguments=positional_arguments,
      keyword_arguments=keyword_arguments,
      keyword_arguments_all=keyword_arguments_all,
      flags=flags,
      warnings=warnings,
    )


def parse_message(text: str | None, prefix: str = "$") -> ParsedMessage:
  return Parser(prefix=prefix).parse(text)


__all__ = ["ParsedArguments", "ParsedMessage", "Parser", "parse_message", "parse_arguments"]