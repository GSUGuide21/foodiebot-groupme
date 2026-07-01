from __future__ import annotations

from typing import Any

from client.commands.base import Command
from client.preconditions.extensions.group_only import GroupOnlyPrecondition
from client.manager import CalendarManager
from client.util import resolve_text

def calendar_usage(prefix: str) -> str:
  return (
    f"Usage: {prefix}calendar <list|create|delete> [options]. "
    f"Examples: {prefix}calendar list [page=1], "
    f"{prefix}calendar create name=\"Dinner\" start_at=1730415600, "
    f"{prefix}calendar delete <event_id>"
  )


def calendar_list_result(events: list[dict[str, str | int | bool]]) -> str:
  if not events:
    return "calendar: no upcoming events found."

  lines = ["calendar: upcoming events"]
  for event in events[:10]:
    event_id = str(event.get("event_id") or event.get("id") or "unknown")
    name = str(event.get("name") or "(unnamed)")
    start_at = event.get("start_at")
    lines.append(f"- {event_id}: {name} (start_at={start_at})")
  return "\n".join(lines)


def calendar_create_result(event_id: str, name: str) -> str:
  return f"calendar: created event {event_id} ('{name}')."


def calendar_delete_result(event_id: str) -> str:
  return f"calendar: deleted event {event_id}."


class CalendarCommand(Command):
  name = "calendar"
  aliases = ["cal", "events"]
  preconditions = [GroupOnlyPrecondition()]
  description = "List, create, or delete group calendar events"
  timeout_seconds = 10

  def execute(self, message, context):
    if not context.group_id or not context.token:
      raise ValueError("calendar: missing group context or access token.")

    if not message.positional_arguments:
      raise ValueError(calendar_usage(context.prefix))

    action = str(message.positional_arguments[0]).strip().lower()
    manager = CalendarManager(str(context.group_id), token=context.token)

    if action in {"list", "ls"}:
      page_value = message.keyword_arguments.get("page", "1")
      try:
        page = max(1, int(page_value))
      except ValueError:
        raise ValueError(calendar_usage(context.prefix))

      response = manager.list_events(page=page)
      events = self._extract_events(response)
      return calendar_list_result(events)

    if action in {"create", "new", "add"}:
      payload = self._build_create_payload(message, context.prefix)
      response = manager.create_event(**payload)
      event_id = self._extract_event_id(response)
      event_name = str(payload.get("name") or "(unnamed)")
      return calendar_create_result(event_id, event_name)

    if action in {"delete", "remove", "rm"}:
      event_id = self._resolve_event_id(message)
      if not event_id:
        raise ValueError(calendar_usage(context.prefix))

      manager.delete_event(event_id=event_id)
      return calendar_delete_result(event_id)

    raise ValueError(calendar_usage(context.prefix))

  def _extract_events(self, response: Any) -> list[dict[str, str | int | bool]]:
    if isinstance(response, dict):
      if isinstance(response.get("events"), list):
        return [event for event in response["events"] if isinstance(event, dict)]
      if isinstance(response.get("response"), dict):
        nested = response["response"].get("events")
        if isinstance(nested, list):
          return [event for event in nested if isinstance(event, dict)]

    if isinstance(response, list):
      return [event for event in response if isinstance(event, dict)]

    return []


  def _build_create_payload(self, message, prefix: str) -> dict[str, Any]:
    kwargs = message.keyword_arguments

    name = str(kwargs.get("name", "")).strip()
    start_at = kwargs.get("start_at")
    if not name or start_at is None:
      raise ValueError(calendar_usage(prefix))

    try:
      start_timestamp = int(str(start_at).strip())
    except ValueError:
      raise ValueError(calendar_usage(prefix))

    is_all_day_flag = message.has_flag("is_all_day") if hasattr(message, "has_flag") else False

    payload: dict[str, Any] = {
      "name": name,
      "start_at": start_timestamp,
      "description": str(kwargs.get("description", "")).strip(),
      "timezone": str(kwargs.get("timezone", "UTC")).strip() or "UTC",
      "is_all_day": is_all_day_flag or self._to_bool(kwargs.get("is_all_day", "false")),
      "reminders": self._parse_reminders(message),
    }

    location_name = str(kwargs.get("location_name", "")).strip()
    if location_name:
      payload["location"] = {
        "name": location_name,
        "lat": kwargs.get("lat"),
        "lng": kwargs.get("lng"),
      }

    end_at = kwargs.get("end_at")
    if end_at is not None and str(end_at).strip() != "":
      try:
        payload["end_at"] = int(str(end_at).strip())
      except ValueError:
        raise ValueError(calendar_usage(prefix))

    return payload


  def _parse_reminders(self, message) -> list[dict[str, int]]:
    values: list[str] = []

    if hasattr(message, "get_keywords"):
      values.extend(message.get_keywords("reminder"))
      values.extend(message.get_keywords("reminders"))

    for key in ("reminder", "reminders"):
      fallback = message.keyword_arguments.get(key)
      if fallback and fallback not in values:
        values.append(str(fallback))

    reminder_seconds: list[int] = []
    for value in values:
      text = str(value).strip()
      if not text:
        continue

      for part in text.split(","):
        candidate = part.strip()
        if not candidate:
          continue
        try:
          seconds = int(candidate)
        except ValueError:
          continue
        if seconds >= 0:
          reminder_seconds.append(seconds)

    return [{"minutes_before": seconds // 60} for seconds in reminder_seconds]


  def _resolve_event_id(self, message) -> str:
    return resolve_text(message, positional_index=1, keyword_keys=("event_id", "id"))


  def _extract_event_id(self, response: Any) -> str:
    if isinstance(response, dict):
      event_id = response.get("event_id") or response.get("id")
      if event_id:
        return str(event_id)

      nested = response.get("event")
      if isinstance(nested, dict):
        nested_id = nested.get("event_id") or nested.get("id")
        if nested_id:
          return str(nested_id)

    return "unknown"


  def _to_bool(self, value: Any) -> bool:
    if isinstance(value, bool):
      return value

    normalized = str(value).strip().lower()
    return normalized in {"1", "true", "yes", "y", "on"}
