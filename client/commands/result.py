from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CommandResult:
  text: str = ""
  attachments: list[dict[str, Any]] = field(default_factory=list)


type CommandResultLike = str | None | CommandResult | dict[str, Any]


def normalize_command_result(value: CommandResultLike) -> CommandResult | None:
  if value is None:
    return None

  if isinstance(value, CommandResult):
    return value

  if isinstance(value, str):
    return CommandResult(text=value)

  if isinstance(value, dict):
    text_value = value.get("text")
    if text_value is None:
      text_value = value.get("reply")
    if text_value is None:
      text_value = value.get("message")

    attachments_value = value.get("attachments", [])
    attachments: list[dict[str, Any]] = []
    if isinstance(attachments_value, list):
      attachments = [item for item in attachments_value if isinstance(item, dict)]

    return CommandResult(
      text="" if text_value is None else str(text_value),
      attachments=attachments,
    )

  return CommandResult(text=str(value))


__all__ = ["CommandResult", "CommandResultLike", "normalize_command_result"]