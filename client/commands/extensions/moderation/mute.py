from __future__ import annotations

from client.commands.base import Command
from client.preconditions.extensions.admin_only import AdminOnlyPrecondition
from client.preconditions.extensions.group_only import GroupOnlyPrecondition
from client.manager import Group, Member
from client.util import resolve_text, usage_error

def mute_result(membership_id: str) -> str:
  return f"mute: muted membership {membership_id} from sending messages."

class MuteCommand(Command):
  name = "mute"
  aliases = ["silence"]
  preconditions = [
    AdminOnlyPrecondition(),
    GroupOnlyPrecondition()
  ]
  description = "Mute a member from sending messages by membership ID"
  timeout_seconds = 8
  muted_members = set()

  def execute(self, message, context):
    if not context.group_id or not context.token:
      raise ValueError("mute: missing group context or access token.")

    membership_id = resolve_text(
      message,
      keyword_keys=("membership_id", "member_id", "id"),
    )
    if not membership_id:
      raise usage_error(context.prefix, "mute", "<membership_id>")

    group = Group(context.group_id, token=context.token)
    member = Member(id=membership_id, group=group, token=context.token)
    self.muted_members.add(member)
    return mute_result(membership_id)