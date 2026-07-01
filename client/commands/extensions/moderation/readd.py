from __future__ import annotations

from client.commands.base import Command
from client.manager import Group
from client.util import clean_text, format_usage, joined_positional_text, resolve_text

def readd_result(user_id: str, nickname: str, results_id: str | None = None) -> str:
  if results_id:
    return f"readd: requested re-add for user {user_id} as '{nickname}' (results_id={results_id})."
  return f"readd: requested re-add for user {user_id} as '{nickname}'."

class ReaddCommand(Command):
  name = "readd"
  aliases = ["addback"]
  description = "Request re-adding a user by user ID and nickname"
  timeout_seconds = 10

  def execute(self, message, context):
    if not context.group_id or not context.token:
      raise ValueError("readd: missing group context or access token.")

    user_id = resolve_text(message, keyword_keys=("user_id", "user"))
    nickname = joined_positional_text(message, start_index=1) or resolve_text(
      message,
      keyword_keys=("nickname", "name", "nick"),
    )
    guid = clean_text(message.keyword_arguments.get("guid", "")) or None

    if not user_id or not nickname:
      raise ValueError(
        f"{format_usage(context.prefix, 'readd', '<user_id> <nickname>')} | "
        f"{format_usage(context.prefix, 'readd', 'user_id=<id> nickname=\"Name\" [guid=<guid>]')}"
      )

    group = Group(context.group_id, token=context.token)
    result = group.readd_member(user_id=user_id, nickname=nickname, guid=guid)

    results_id = None
    if isinstance(result, dict):
      results_id = result.get("results_id")

    return readd_result(user_id=user_id, nickname=nickname, results_id=results_id)
