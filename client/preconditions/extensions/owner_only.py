from __future__ import annotations

from client.manager import Group
from client.preconditions.base import Precondition


class OwnerOnlyPrecondition(Precondition):
  name = "owner_only"
  description = "Allows only the group owner to execute the command"
  priority = 10

  def execute(self, message, context) -> tuple[bool, str]:
    group_id = str(context.group_id or "").strip()
    if not group_id:
      return False, "This command can only be used in a group."

    sender_id = str(context.sender_id or "").strip()
    if not sender_id:
      return False, "This command is restricted to the group owner."

    try:
      group = Group(group_id, token=context.token)
      payload = group.get()
    except Exception as exc:
      return False, f"owner_only: unable to verify group owner: {exc}"

    owner_id = ""
    if isinstance(payload, dict):
      owner_value = payload.get("owner_id") or payload.get("ownerId")
      if owner_value is not None:
        owner_id = str(owner_value).strip()
      elif isinstance(payload.get("owner"), dict):
        owner = payload["owner"]
        owner_id = str(owner.get("user_id") or owner.get("id") or "").strip()

    if not owner_id:
      for member in group.get_members():
        roles = member.get("roles") or []
        if any(str(role).lower() == "owner" for role in roles):
          owner_id = str(member.get("user_id") or member.get("id") or "").strip()
          break

    if not owner_id:
      return False, "owner_only: could not determine the group owner."

    if sender_id == owner_id:
      return True, ""

    return False, "This command is restricted to the group owner."
