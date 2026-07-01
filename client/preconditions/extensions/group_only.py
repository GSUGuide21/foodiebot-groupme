from __future__ import annotations

from client.preconditions.base import Precondition


class GroupOnlyPrecondition(Precondition):
  name = "group_only"
  description = "Allows only messages sent from a group"
  priority = 10

  def execute(self, message, context) -> tuple[bool, str]:
    if str(context.group_id).strip():
      return True, ""
    return False, "This command can only be used in a group."
