from __future__ import annotations


def format_usage(prefix: str, command: str, syntax: str = "") -> str:
  usage = f"Usage: {prefix}{command}"
  if syntax:
    usage = f"{usage} {syntax}"

  return usage


def usage_error(prefix: str, command: str, syntax: str = "") -> ValueError:
  return ValueError(format_usage(prefix, command, syntax))
