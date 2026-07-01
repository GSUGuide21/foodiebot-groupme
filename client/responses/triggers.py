from __future__ import annotations

from dataclasses import dataclass
import re


def _normalize_text(text: str) -> str:
  lowered = text.lower().strip()
  lowered = re.sub(r"[^a-z0-9\s]", "", lowered)
  return re.sub(r"\s+", " ", lowered).strip()


@dataclass(slots=True)
class ParsedTrigger:
  name: str
  matched_text: str = ""
  trigger_text: str = ""


@dataclass(slots=True)
class _RegisteredTrigger:
  response_name: str
  response_priority: int
  response_order: int
  trigger_index: int
  trigger_text: str


class TriggerParser:
  def __init__(self) -> None:
    self._triggers: dict[str, list[_RegisteredTrigger]] = {}
    self._response_order: dict[str, int] = {}
    self._next_response_order = 0

  def register(
    self,
    name: str,
    triggers: list[str] | None = None,
    priority: int = 0,
  ) -> None:
    response_name = name.lower().strip()
    if not response_name:
      return

    if response_name not in self._response_order:
      self._response_order[response_name] = self._next_response_order
      self._next_response_order += 1

    response_order = self._response_order[response_name]
    registered_triggers: list[_RegisteredTrigger] = []

    for trigger_index, trigger in enumerate(triggers or []):
      normalized_trigger = _normalize_text(trigger)
      if not normalized_trigger:
        continue

      registered_triggers.append(
        _RegisteredTrigger(
          response_name=response_name,
          response_priority=priority,
          response_order=response_order,
          trigger_index=trigger_index,
          trigger_text=normalized_trigger,
        )
      )

    self._triggers[response_name] = registered_triggers

  def parse(self, text: str | None) -> ParsedTrigger | None:
    normalized_text = _normalize_text(str(text or ""))
    if not normalized_text:
      return None

    best_match: tuple[tuple[int, int, int, int], ParsedTrigger] | None = None

    for triggers in self._triggers.values():
      for trigger in triggers:
        trigger_pattern = rf"(?<!\w){re.escape(trigger.trigger_text)}(?!\w)"
        match = re.search(trigger_pattern, normalized_text, re.IGNORECASE)
        if not match:
          continue

        sort_key = (
          -trigger.response_priority,
          -len(trigger.trigger_text),
          trigger.response_order,
          trigger.trigger_index,
        )

        parsed = ParsedTrigger(
          name=trigger.response_name,
          matched_text=match.group(0),
          trigger_text=trigger.trigger_text,
        )

        if best_match is None or sort_key < best_match[0]:
          best_match = (sort_key, parsed)

    return None if best_match is None else best_match[1]


__all__ = ["ParsedTrigger", "TriggerParser"]