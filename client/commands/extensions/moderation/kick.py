from __future__ import annotations

from client.commands.base import Command
from client.manager import Group, Member
from client.preconditions.extensions.admin_only import AdminOnlyPrecondition
from client.preconditions.extensions.group_only import GroupOnlyPrecondition
from client.preconditions.extensions.not_self import NotSelfPrecondition
from client.util import resolve_text, usage_error

def kick_result(membership_id: str) -> str:
  return f"kick: removed membership {membership_id}."

class KickCommand(Command):
  name = "kick"
  aliases = ["remove"]
  preconditions = [
    GroupOnlyPrecondition(),
    AdminOnlyPrecondition(),
    NotSelfPrecondition()
  ]
  description = "Remove a member by membership ID or @mention"
  timeout_seconds = 8

  def execute(self, message, context):
    if not context.group_id or not context.token:
      raise ValueError("kick: missing group context or access token.")

    group = Group(context.group_id, token=context.token)

    membership_id = resolve_text(
      message,
      keyword_keys=("membership_id", "member_id", "id"),
    )
    if not membership_id:
      mentioned_members = self.resolve_members_from_mention(context.raw_message, group)
      if mentioned_members:
        membership_id = str(mentioned_members[0].get("id") or "").strip()
    if not membership_id:
      raise usage_error(context.prefix, "kick", "<membership_id|@mention>")

    member = Member(id=membership_id, group=group, token=context.token)
    member.kick()
    return kick_result(membership_id)
