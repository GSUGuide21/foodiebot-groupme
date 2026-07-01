from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Pattern

TargetSpec = str | Pattern[str]


@dataclass(slots=True)
class ParsedResponse:
  name: str
  matched_text: str = ""
  target_pattern: str = ""


@dataclass(slots=True)
class _RegisteredTarget:
  response_name: str
  response_priority: int
  response_order: int
  target_index: int
  is_exact: bool
  exact_text: str = ""
  pattern: Pattern[str] | None = None


class ResponseParser:
  def __init__(self) -> None:
    self._targets: dict[str, list[_RegisteredTarget]] = {}
    self._response_order: dict[str, int] = {}
    self._next_response_order = 0

  def register(
    self,
    name: str,
    targets: list[TargetSpec] | None = None,
    priority: int = 0,
  ) -> None:
    response_name = name.lower().strip()
    if not response_name:
      return

    if response_name not in self._response_order:
      self._response_order[response_name] = self._next_response_order
      self._next_response_order += 1

    response_order = self._response_order[response_name]
    registered_targets: list[_RegisteredTarget] = []

    for target_index, target in enumerate(targets or []):
      if isinstance(target, str):
        normalized_target = target.strip()
        if not normalized_target:
          continue

        registered_targets.append(
          _RegisteredTarget(
            response_name=response_name,
            response_priority=priority,
            response_order=response_order,
            target_index=target_index,
            is_exact=True,
            exact_text=normalized_target.lower(),
          )
        )
        continue

      if isinstance(target, re.Pattern):
        registered_targets.append(
          _RegisteredTarget(
            response_name=response_name,
            response_priority=priority,
            response_order=response_order,
            target_index=target_index,
            is_exact=False,
            pattern=target,
          )
        )

    self._targets[response_name] = registered_targets

  def parse(self, text: str | None) -> ParsedResponse | None:
    normalized_text = str(text or "").strip()
    if not normalized_text:
      return None

    lowered_text = normalized_text.lower()

    best_match: tuple[tuple[int, int, int, int], ParsedResponse] | None = None

    for targets in self._targets.values():
      for target in targets:
        matched_text = ""
        target_pattern = ""

        if target.is_exact:
          if lowered_text != target.exact_text:
            continue
          matched_text = normalized_text
          target_pattern = target.exact_text
        else:
          if target.pattern is None:
            continue
          match = target.pattern.search(normalized_text)
          if not match:
            continue
          matched_text = match.group(0)
          target_pattern = target.pattern.pattern

        # Higher response priority first, then exact target matches before regex,
        # then stable registration and declaration order.
        sort_key = (
          -target.response_priority,
          0 if target.is_exact else 1,
          target.response_order,
          target.target_index,
        )

        parsed = ParsedResponse(
          name=target.response_name,
          matched_text=matched_text,
          target_pattern=target_pattern,
        )

        if best_match is None or sort_key < best_match[0]:
          best_match = (sort_key, parsed)

    return None if best_match is None else best_match[1]


__all__ = ["ParsedResponse", "ResponseParser", "TargetSpec"]
