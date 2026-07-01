from __future__ import annotations

from client.preconditions.base import Precondition
from client.util import resolve_text


class NotSelfPrecondition(Precondition):
  name = "not_self"
  description = "Prevents a command from targeting the sender"
  priority = 10

  def execute(self, message, context) -> tuple[bool, str]:
    target_id = resolve_text(
      message,
      keyword_keys=("target_id", "user_id", "member_id", "id", "user"),
    ).strip()

    if not target_id:
      return True, ""

    sender_id = str(context.sender_id or "").strip()
    if sender_id and target_id == sender_id:
      return False, "You cannot target yourself with this command."

    return True, ""
