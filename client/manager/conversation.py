from __future__ import annotations

from typing import Any

from .base import Manager


class ConversationManager(Manager):
  v4_base_url = "https://api.groupme.com/v4"

  def __init__(self, conversation_id: str | None = None, **options: Any):
    super().__init__(path="", **options)
    self.conversation_id = "" if conversation_id is None else str(conversation_id)

  def get_message(self, message_id: str, group_id: str | None = None):
    resolved_group_id = self._require_conversation_id(group_id)
    path = f"{self.v4_base_url}/groups/{resolved_group_id}/messages/{message_id}"
    response = self.GET(path=path, headers=self._headers())
    payload = self._json_response_or_payload(response)
    if isinstance(payload, dict) and isinstance(payload.get("message"), dict):
      return payload.get("message")
    return payload

  def edit_message(
    self,
    message_id: str,
    text: str | None = None,
    attachments: list[dict[str, Any]] | None = None,
    group_id: str | None = None,
  ):
    resolved_group_id = self._require_conversation_id(group_id)
    normalized_text = None if text is None else str(text)
    normalized_attachments = attachments or []

    if normalized_text is None and not normalized_attachments:
      raise ValueError("edit_message requires text or at least one attachment")

    payload: dict[str, Any] = {}
    if normalized_text is not None:
      payload["text"] = normalized_text
    if normalized_attachments:
      payload["attachments"] = normalized_attachments

    path = f"{self.v4_base_url}/groups/{resolved_group_id}/messages/{message_id}"
    response = self.PUT(path=path, headers=self._headers(), json=payload)
    payload = self._json_response_or_payload(response)
    if isinstance(payload, dict) and isinstance(payload.get("message"), dict):
      return payload.get("message")
    return payload

  def delete_message(self, message_id: str, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/messages/{message_id}"
    response = self.DELETE(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def delete_group_message_legacy(self, message_id: str, group_id: str | None = None):
    resolved_group_id = self._require_conversation_id(group_id)
    path = f"/groups/{resolved_group_id}/messages/{message_id}/delete"
    response = self.POST(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def like_message(
    self,
    message_id: str,
    like_icon: dict[str, Any] | None = None,
    conversation_id: str | None = None,
  ):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/messages/{resolved_conversation_id}/{message_id}/like"
    payload = {"like_icon": like_icon} if like_icon else None
    response = self.POST(path=path, headers=self._headers(), json=payload)
    return self._json_response_or_payload(response)

  def unlike_message(self, message_id: str, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/messages/{resolved_conversation_id}/{message_id}/unlike"
    response = self.POST(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def pin_message(self, message_id: str, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/messages/{message_id}/pin"
    response = self.POST(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def unpin_message(self, message_id: str, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/messages/{message_id}/unpin"
    response = self.POST(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def list_group_pins(self, group_id: str | None = None):
    resolved_group_id = self._require_conversation_id(group_id)
    path = f"/pinned/groups/{resolved_group_id}/messages"
    response = self.GET(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def list_dm_pins(self, other_user_id: str):
    params = {"other_user_id": str(other_user_id)}
    response = self.GET(path="/pinned/direct_messages", headers=self._headers(), params=params)
    return self._json_response_or_payload(response)

  def list_events(
    self,
    end_at: str,
    limit: int = 20,
    conversation_id: str | None = None,
  ):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    params = {
      "end_at": str(end_at),
      "limit": max(1, int(limit)),
    }
    path = f"/conversations/{resolved_conversation_id}/events/list"
    response = self.GET(path=path, headers=self._headers(), params=params)
    return self._json_response_or_payload(response)

  def show_event(self, event_id: str, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    params = {"event_id": str(event_id)}
    path = f"/conversations/{resolved_conversation_id}/events/show"
    response = self.GET(path=path, headers=self._headers(), params=params)
    return self._json_response_or_payload(response)

  def create_event(self, conversation_id: str | None = None, **event_payload: Any):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/events/create"
    response = self.POST(path=path, headers=self._headers(), json=event_payload)
    return self._json_response_or_payload(response)

  def update_event(self, event_id: str, conversation_id: str | None = None, **event_payload: Any):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/events/update"
    params = {"event_id": str(event_id)}
    response = self.POST(path=path, headers=self._headers(), params=params, json=event_payload)
    return self._json_response_or_payload(response)

  def delete_event(self, event_id: str, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/events/delete"
    params = {"event_id": str(event_id)}
    response = self.DELETE(path=path, headers=self._headers(), params=params)
    return self._json_response_or_payload(response)

  def rsvp_event(self, event_id: str, going: bool, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/events/rsvp"
    params = {
      "event_id": str(event_id),
      "going": str(bool(going)).lower(),
    }
    response = self.POST(path=path, headers=self._headers(), params=params)
    return self._json_response_or_payload(response)

  def clear_rsvp(self, event_id: str, conversation_id: str | None = None):
    resolved_conversation_id = self._require_conversation_id(conversation_id)
    path = f"/conversations/{resolved_conversation_id}/events/rsvp/delete"
    params = {"event_id": str(event_id)}
    response = self.DELETE(path=path, headers=self._headers(), params=params)
    return self._json_response_or_payload(response)

  def likes_leaderboard(self, period: str = "week", group_id: str | None = None):
    resolved_group_id = self._require_conversation_id(group_id)
    normalized_period = str(period).strip().lower()
    if normalized_period not in {"day", "week", "month"}:
      raise ValueError("period must be one of: day, week, month")

    path = f"/groups/{resolved_group_id}/likes"
    response = self.GET(path=path, headers=self._headers(), params={"period": normalized_period})
    return self._json_response_or_payload(response)

  def my_likes(self, group_id: str | None = None):
    resolved_group_id = self._require_conversation_id(group_id)
    path = f"/groups/{resolved_group_id}/likes/mine"
    response = self.GET(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def my_hits(self, group_id: str | None = None):
    resolved_group_id = self._require_conversation_id(group_id)
    path = f"/groups/{resolved_group_id}/likes/for_me"
    response = self.GET(path=path, headers=self._headers())
    return self._json_response_or_payload(response)

  def _headers(self) -> dict[str, Any]:
    return {"X-Access-Token": self.token}

  def _require_conversation_id(self, conversation_id: str | None = None) -> str:
    resolved = self.conversation_id if conversation_id is None else str(conversation_id)
    resolved = str(resolved).strip()
    if not resolved:
      raise ValueError("conversation_id is required")
    return resolved

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
