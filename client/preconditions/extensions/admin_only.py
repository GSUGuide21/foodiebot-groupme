from __future__ import annotations

from client.preconditions.base import Precondition

class AdminOnlyPrecondition(Precondition):
  name = "admin_only"
  description = "Allows only admins to execute the command"
  priority = 10

  def execute(self, message, context) -> tuple[bool, str]:
    if context.sender_id in context.token.admin_ids:
      return True, ""
    return False, "This command is restricted to admins only."