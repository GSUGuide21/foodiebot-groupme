from __future__ import annotations

from datetime import datetime
from typing import Any

from .group import Group
from .member import Member


class Message:
  @staticmethod
  def _resolve_conversation_id(raw_message: dict[str, Any]) -> str:
    candidates = (
      raw_message.get("subgroup_id"),
      raw_message.get("group_id"),
      raw_message.get("chat_id"),
      raw_message.get("conversation_id"),
      raw_message.get("source_guid"),
    )
    for value in candidates:
      if value is not None and str(value).strip():
        return str(value)

    group_obj = raw_message.get("group")
    if isinstance(group_obj, dict):
      for key in ("group_id", "id"):
        value = group_obj.get(key)
        if value is not None and str(value).strip():
          return str(value)

    subgroup_obj = raw_message.get("subgroup")
    if isinstance(subgroup_obj, dict):
      value = subgroup_obj.get("id")
      if value is not None and str(value).strip():
        return str(value)

    return ""

  def __init__(self, raw: dict[str, Any] | None = None, text: str | None = None):
    raw_message = raw or {"attachments": []}
    self.raw: dict[str, Any] = raw_message

    text_value = text if text is not None else raw_message.get("text")
    self.text: str = "" if text_value is None else str(text_value)

    user_id_value = raw_message.get("user_id")
    self.user_id: str = "" if user_id_value is None else str(user_id_value)

    name_value = raw_message.get("name")
    self.name: str = "" if name_value is None else str(name_value)

    sender_type_value = raw_message.get("sender_type", "user")
    self.sender_type: str = str(sender_type_value)

    self.group_id: str = self._resolve_conversation_id(raw_message)

    avatar_url_value = raw_message.get("avatar_url")
    self.avatar_url: str = "" if avatar_url_value is None else str(avatar_url_value)

    created_at = raw_message.get("created_at")
    if isinstance(created_at, (int, float)):
      self.time: datetime = datetime.fromtimestamp(created_at)
    elif isinstance(created_at, datetime):
      self.time = created_at
    else:
      self.time = datetime.now()

  def __repr__(self):
    return f"({self.group_id}) {self.name}: {self.text}"

  def __getitem__(self, key: str):
    return getattr(self, key)

  def __setitem__(self, name: str, value: Any):
    return setattr(self, name, value)

  @property
  def group(self) -> Group:
    return Group(self.group_id)

  @property
  def sender(self) -> Member:
    return Member(
      group=self.group,
      user_id=self.user_id,
      user={
        "name": self.name,
        "user_id": self.user_id,
        "avatar_url": self.avatar_url,
      },
    )

  @property
  def attachments(self) -> list[dict[str, Any]]:
    attachments = self.raw.get("attachments", [])
    if not isinstance(attachments, list):
      return []
    return [attachment for attachment in attachments if isinstance(attachment, dict)]

  @property
  def image_url(self) -> str:
    images = [attachment for attachment in self.attachments if attachment["type"] == "image"]
    if images and len(images) > 0:
      return str(images.pop(0).get("url", ""))
    return ""

  @property
  def mentions(self) -> dict[str, Any]:
    mentions = [attachment for attachment in self.attachments if attachment["type"] == "mentions"]
    if mentions and len(mentions) > 0:
      mention = mentions.pop(0)
      return {
        "user_ids": mention.get("user_ids", []),
        "loci": mention.get("loci", []),
      }
    return {}

  @property
  def reply(self) -> str | None:
    replies = [attachment for attachment in self.attachments if attachment["type"] == "reply"]
    if replies and len(replies) > 0:
      reply_id = replies.pop(0).get("reply_id")
      return None if reply_id is None else str(reply_id)
    return None
  
  def delete(self, token: str | None = None):
    group = Group(self.group_id, token=token)
    message_id = self.raw.get("message_id")
    if message_id is None:
      return None
    return group.delete_message(str(message_id))