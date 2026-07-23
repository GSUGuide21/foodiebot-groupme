from __future__ import annotations

from client.preconditions.base import Precondition
from client.util import resolve_text


def _has_sender_mention(raw_message: dict[str, object] | None, sender_id: str) -> bool:
  if not sender_id or not isinstance(raw_message, dict):
    return False

  attachments = raw_message.get("attachments")
  if not isinstance(attachments, list):
    return False

  for attachment in attachments:
    if not isinstance(attachment, dict) or attachment.get("type") != "mentions":
      continue

    user_ids = attachment.get("user_ids")
    if not isinstance(user_ids, list):
      continue

    if sender_id in {str(user_id).strip() for user_id in user_ids if user_id is not None}:
      return True

  return False


class NotSelfPrecondition(Precondition):
  name = "not_self"
  description = "Prevents a command from targeting the sender"
  priority = 10

  def execute(self, message, context) -> tuple[bool, str]:
    target_id = resolve_text(
      message,
      keyword_keys=("target_id", "user_id", "member_id", "id", "user"),
    ).strip()

    sender_id = str(context.sender_id or "").strip()
    if _has_sender_mention(getattr(context, "raw_message", None), sender_id):
      return False, "You cannot target yourself with this command."

    if not target_id:
      return True, ""

    if sender_id and target_id == sender_id:
      return False, "You cannot target yourself with this command."

    return True, ""
