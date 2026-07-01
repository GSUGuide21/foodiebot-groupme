from __future__ import annotations

from typing import Any

from .base import Manager


class CalendarManager(Manager):
  def __init__(self, group_id: str, **options: Any):
    super().__init__(path="conversations", **options)
    self.group_id = group_id

  @property
  def events_path(self) -> str:
    return f"/{self.group_id}/events"

  def list_events(self, page: int = 1):
    headers = {"X-Access-Token": self.token}
    params = {"page": page}
    response = self.GET(path=self.events_path, headers=headers, params=params)
    return self._json_response_or_payload(response)

  def create_event(self, **event_payload: Any):
    headers = {"X-Access-Token": self.token}
    response = self.POST(path=self.events_path, headers=headers, json=event_payload)
    return self._json_response_or_payload(response)

  def delete_event(self, event_id: str):
    headers = {"X-Access-Token": self.token}
    response = self.DELETE(path=f"{self.events_path}/{event_id}", headers=headers)
    return self._json_response_or_payload(response)

  @staticmethod
  def _json_response_or_payload(response: Any):
    if response is None:
      return None

    try:
      payload = response.json()
    except ValueError:
      return None

    if not isinstance(payload, dict):
      return payload

    if "response" in payload:
      return payload.get("response")

    return payload
