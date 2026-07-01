from __future__ import annotations

from typing import Any


def clean_text(value: Any) -> str:
  return str(value).strip()


def positional_text(message, index: int = 0) -> str:
  if len(message.positional_arguments) <= index:
    return ""

  return clean_text(message.positional_arguments[index])


def keyword_text(message, *keys: str) -> str:
  for key in keys:
    value = message.keyword_arguments.get(key)
    if value is None:
      continue

    normalized = clean_text(value)
    if normalized:
      return normalized

  return ""


def resolve_text(message, *, positional_index: int = 0, keyword_keys: tuple[str, ...] = ()) -> str:
  from_position = positional_text(message, index=positional_index)
  if from_position:
    return from_position

  return keyword_text(message, *keyword_keys)


def joined_positional_text(message, start_index: int = 0) -> str:
  values = [clean_text(item) for item in message.positional_arguments[start_index:]]
  return " ".join(value for value in values if value).strip()
