from __future__ import annotations

import os
from typing import Any

from client.commands import CommandRouter
from client.commands.result import normalize_command_result
from client.manager import BotManager
from client.responses import ResponseRouter
from client.responses.result import normalize_response_result


class Client:
  @staticmethod
  def _resolve_conversation_id(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
      return ""

    candidates = (
      payload.get("subgroup_id"),
      payload.get("group_id"),
      payload.get("chat_id"),
      payload.get("conversation_id"),
      payload.get("source_guid"),
    )
    for value in candidates:
      if value is not None and str(value).strip():
        return str(value)

    group_obj = payload.get("group")
    if isinstance(group_obj, dict):
      for key in ("group_id", "id"):
        value = group_obj.get(key)
        if value is not None and str(value).strip():
          return str(value)

    subgroup_obj = payload.get("subgroup")
    if isinstance(subgroup_obj, dict):
      value = subgroup_obj.get("id")
      if value is not None and str(value).strip():
        return str(value)

    return ""

  def __init__(self, **data: Any):
    bot_id = data.get("bot_id")
    app_id = data.get("app_id")
    token = data.get("token")
    prefix = data.get("prefix")
    max_messages = data.get("max_messages")

    self.bot_id = str(bot_id if bot_id is not None else os.environ.get("bot_id") or "")
    self.app_id = str(app_id if app_id is not None else os.environ.get("app_id") or "")
    self.token = token if token is not None else os.environ.get("token")
    self.prefix = str(prefix if prefix is not None else os.environ.get("prefix") or "$")
    self.max_messages = int(max_messages if max_messages is not None else os.environ.get("max_messages") or 1000)

    self.command_router = data.get("command_router") or CommandRouter(prefix=self.prefix)
    self.response_router = data.get("response_router") or ResponseRouter()
    self.group_id = data.get("group_id")
    self.group = data.get("group")
    self.bot_manager = BotManager(token=self.token)

  def setup(self, **data: Any) -> "Client":
    if "bot_id" in data:
      self.bot_id = str(data["bot_id"] or "")
    if "app_id" in data:
      self.app_id = str(data["app_id"] or "")
    if "token" in data:
      self.token = data["token"]
    if "prefix" in data:
      self.prefix = str(data["prefix"] or "$")
      self.command_router.set_prefix(self.prefix)
    if "response_router" in data:
      self.response_router = data["response_router"]
    if "max_messages" in data:
      self.max_messages = int(data["max_messages"] or 1000)
    if "token" in data:
      self.bot_manager.token = self.token

    return self

  def dispatch(self, **data: Any):
    group_id = self._resolve_conversation_id(data) or os.environ.get("group_id")
    if not group_id:
      return None

    self.group_id = group_id
    self.group = data.get("group", {"group_id": group_id})
    return self.send_init_msg()

  def send_init_msg(self):
    return self.respond(reply="Hey, I'm FoodieBot! I'm going to be your friend today.")

  def respond(self, **data: Any):
    reply = data.get("reply", "")
    if reply is None:
      return None

    text = str(reply).strip()
    if not text:
      return None

    print(text)

    if not self.bot_id:
      return None

    payload: dict[str, Any] = {
      "bot_id": self.bot_id,
      "text": text,
    }

    attachments = data.get("attachments")
    if attachments:
      payload["attachments"] = attachments

    return self.bot_manager.POST(path="/post", json=payload, timeout=10)

  def reply(self, **message: Any):
    sender_type = message.get("sender_type")
    if sender_type == "bot":
      return None

    text = message.get("text")
    sender_id = str(
      message.get("user_id")
      or message.get("sender_id")
      or message.get("sender_name")
      or ""
    )
    sender_name = str(message.get("name") or message.get("sender_name") or "")
    group_id = self._resolve_conversation_id(message) or str(
      self.group_id
      or os.environ.get("group_id")
      or ""
    )
    message_id = str(message.get("message_id") or message.get("id") or "")
    token = str(self.token or os.environ.get("token") or "")

    response_output = self.response_router.handle(
      text,
      sender_id=sender_id,
      sender_name=sender_name,
      group_id=group_id,
      message_id=message_id,
      token=token,
    )
    normalized_response = normalize_response_result(response_output)
    if normalized_response is not None:
      return self.respond(
        reply=normalized_response.text,
        attachments=normalized_response.attachments,
      )

    command_output = self.command_router.handle(
      text,
      sender_id=sender_id,
      group_id=group_id,
      token=token,
    )
    normalized = normalize_command_result(command_output)
    if normalized is None:
      return None

    return self.respond(
      reply=normalized.text,
      attachments=normalized.attachments,
    )

FoodieBot = Client

__all__ = ["Client", "FoodieBot"]