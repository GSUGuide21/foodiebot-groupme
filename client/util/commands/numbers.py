from __future__ import annotations

from typing import Any


def normalize_bounds(start: int, end: int) -> tuple[int, int]:
  if start <= end:
    return start, end

  return end, start


def parse_int(name: str, value: Any, *, minimum: int | None = None, maximum: int | None = None) -> int:
  try:
    parsed = int(str(value).strip())
  except (TypeError, ValueError) as exc:
    raise ValueError(f"Invalid {name} value: {value}") from exc

  if minimum is not None and maximum is not None and (parsed < minimum or parsed > maximum):
    raise ValueError(f"{name} must be between {minimum} and {maximum}")
  if minimum is not None and maximum is None and parsed < minimum:
    raise ValueError(f"{name} must be at least {minimum}")
  if maximum is not None and minimum is None and parsed > maximum:
    raise ValueError(f"{name} must be at most {maximum}")

  return parsed
