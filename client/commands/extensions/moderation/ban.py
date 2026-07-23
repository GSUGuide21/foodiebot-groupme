from __future__ import annotations

from client.commands.base import Command
from client.preconditions.extensions.admin_only import AdminOnlyPrecondition
from client.preconditions.extensions.group_only import GroupOnlyPrecondition
from client.manager import Group, Member
from client.util import resolve_text, usage_error

def ban_result(membership_id: str) -> str:
  return f"ban: blocked membership {membership_id} from rejoining."

class BanCommand(Command):
  name = "ban"
  aliases = ["block"]
  preconditions = [
    AdminOnlyPrecondition(),
    GroupOnlyPrecondition()
  ]
  description = "Block a former member from rejoining by membership ID or @mention"
  timeout_seconds = 8

  def execute(self, message, context):
    if not context.group_id or not context.token:
      raise ValueError("ban: missing group context or access token.")

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
      raise usage_error(context.prefix, "ban", "<membership_id|@mention>")

    member = Member(id=membership_id, group=group, token=context.token)
    member.ban()
    return ban_result(membership_id)
