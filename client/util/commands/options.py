from __future__ import annotations


def parse_csv_values(raw: str | None) -> list[str]:
  if raw is None:
    return []

  return [part.strip() for part in str(raw).split(",") if part.strip()]
