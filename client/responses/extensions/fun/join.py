from __future__ import annotations

from client.responses.base import Response
from client.responses.result import ResponseResult
from client.responses.attachments import mentions_attachment


class JoinResponse(Response):
  name = "join"
  description = "Responds when a member joins the chat"
  priority = 10
  triggers = [
    "joined the conversation",
    "joined the chat",
    "joined the group",
    "was added to the group",
  ]

  def execute(self, message, context):
    name = context.sender_name.strip() or "there"
    sender_id = context.sender_id.strip()

    if not sender_id or name == "there":
      return f"Welcome, {name}! Glad you're here."

    mention_label = f"@{name}"
    text = f"Welcome, {mention_label}! Glad you're here."
    start_index = text.find(mention_label)

    if start_index < 0:
      return text

    return ResponseResult(
      text=text,
      attachments=[
        mentions_attachment(
          user_ids=[sender_id],
          loci=[[start_index, len(mention_label)]],
        )
      ],
    )
