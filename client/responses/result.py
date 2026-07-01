from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from client.responses.attachments import image_attachment, sanitize_message_attachments

@dataclass(slots=True)
class ResponseResult:
  text: str = ""
  attachments: list[dict[str, Any]] = field(default_factory=list)

type ResponseResultLike = str | None | ResponseResult | dict[str, Any]

def normalize_response_result(value: ResponseResultLike) -> ResponseResult | None:
  if value is None:
    return None

  if isinstance(value, ResponseResult):
    return value

  if isinstance(value, str):
    return ResponseResult(text=value)

  if isinstance(value, dict):
    text_value = value.get("text")
    if text_value is None:
      text_value = value.get("reply")
    if text_value is None:
      text_value = value.get("message")

    attachments_value = value.get("attachments")
    if attachments_value is None:
      attachments_value = value.get("attachment")

    attachments = sanitize_message_attachments(attachments_value)

    image_url = value.get("image_url")
    if image_url and not attachments:
      attachments = sanitize_message_attachments([image_attachment(str(image_url))])

    return ResponseResult(
      text="" if text_value is None else str(text_value),
      attachments=attachments,
    )

  return ResponseResult(text=str(value))

__all__ = ["ResponseResult", "ResponseResultLike", "normalize_response_result"]