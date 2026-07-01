from __future__ import annotations

from typing import Any

from client.commands.base import Command
from client.manager import Group
from client.responses.attachments import build_mentions_message


def everyone_usage(prefix: str) -> str:
  return f"Usage: {prefix}everyone [optional message]"


class EveryoneCommand(Command):
  name = "everyone"
  aliases = ["all", "tagall"]
  description = "Mention everyone in the current group"
  timeout_seconds = 12

  def execute(self, message, context):
    if not context.group_id or not context.token:
      raise ValueError("everyone: missing group context or access token.")

    group = Group(str(context.group_id), token=context.token)
    members = group.get_members()
    mentionable_users = self._resolve_mentionable_users(members, sender_id=str(context.sender_id or ""))
    if not mentionable_users:
      return "everyone: no members available to mention."

    suffix_text = str(message.arg_text or "").strip()
    text, attachments = self._build_payload_with_limit(
      users=mentionable_users,
      prefix_text="Heads up,",
      suffix_text=suffix_text,
      max_text_length=1000,
    )
    if not attachments:
      return "everyone: message is too long to build valid mentions."

    if not text:
      raise ValueError(everyone_usage(context.prefix))

    return {
      "text": text,
      "attachments": attachments,
    }

  def _resolve_mentionable_users(self, members: list[dict[str, Any]], sender_id: str) -> list[dict[str, str]]:
    users: list[dict[str, str]] = []
    seen_user_ids: set[str] = set()

    normalized_sender_id = sender_id.strip()
    for member in members:
      user_id = str(member.get("user_id") or member.get("id") or "").strip()
      if not user_id:
        continue
      if user_id == normalized_sender_id:
        continue
      if user_id in seen_user_ids:
        continue

      display_name = str(
        member.get("nickname")
        or member.get("name")
        or (member.get("user") or {}).get("name")
        or ""
      ).strip()
      if not display_name:
        display_name = f"user_{user_id[-4:]}"

      users.append({"user_id": user_id, "name": display_name})
      seen_user_ids.add(user_id)

    return users

  def _build_payload_with_limit(
    self,
    users: list[dict[str, str]],
    prefix_text: str,
    suffix_text: str,
    max_text_length: int,
  ) -> tuple[str, list[dict[str, Any]]]:
    best_text = ""
    best_attachments: list[dict[str, Any]] = []

    selected_users: list[dict[str, str]] = []
    for user in users:
      candidate_users = [*selected_users, user]
      text, attachments = build_mentions_message(
        candidate_users,
        prefix_text=prefix_text,
        suffix_text=suffix_text,
      )
      if len(text) > max_text_length:
        break

      selected_users = candidate_users
      best_text = text
      best_attachments = attachments

    return best_text, best_attachments
