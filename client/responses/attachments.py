from __future__ import annotations

from typing import Any

Attachment = dict[str, Any]

_SENDABLE_ATTACHMENT_TYPES = {
  "image",
  "video",
  "file",
  "location",
  "emoji",
  "reply",
  "mentions",
}


def image_attachment(url: str) -> Attachment:
  return {
    "type": "image",
    "url": str(url),
  }


def video_attachment(url: str, preview_url: str) -> Attachment:
  return {
    "type": "video",
    "url": str(url),
    "preview_url": str(preview_url),
  }


def file_attachment(file_id: str) -> Attachment:
  return {
    "type": "file",
    "file_id": str(file_id),
  }


def location_attachment(name: str, lat: str | float, lng: str | float) -> Attachment:
  return {
    "type": "location",
    "name": str(name),
    "lat": str(lat),
    "lng": str(lng),
  }


def emoji_attachment(placeholder: str, charmap: list[list[int]]) -> Attachment:
  return {
    "type": "emoji",
    "placeholder": str(placeholder),
    "charmap": charmap,
  }


def reply_attachment(reply_id: str, base_reply_id: str | None = None) -> Attachment:
  attachment: Attachment = {
    "type": "reply",
    "base_reply_id": str(base_reply_id or reply_id),
  }
  if reply_id:
    attachment["reply_id"] = str(reply_id)
  return attachment


def mentions_attachment(user_ids: list[str], loci: list[list[int]]) -> Attachment:
  return {
    "type": "mentions",
    "user_ids": [str(user_id) for user_id in user_ids],
    "loci": [[int(pair[0]), int(pair[1])] for pair in loci],
  }


def build_mentions_message(
  users: list[dict[str, Any] | tuple[str, str]],
  prefix_text: str = "",
  suffix_text: str = "",
  separator: str = " ",
) -> tuple[str, list[Attachment]]:
  normalized_separator = separator if separator else " "
  text = str(prefix_text or "")

  user_ids: list[str] = []
  loci: list[list[int]] = []
  mention_chunks: list[str] = []

  for user in users:
    user_id = ""
    display_name = ""

    if isinstance(user, tuple) and len(user) >= 2:
      user_id = str(user[0] or "").strip()
      display_name = str(user[1] or "").strip()
    elif isinstance(user, dict):
      user_id = str(user.get("user_id") or user.get("id") or "").strip()
      display_name = str(user.get("name") or user.get("nickname") or "").strip()

    if not user_id or not display_name:
      continue

    mention_name = display_name[1:] if display_name.startswith("@") else display_name
    mention_chunks.append(f"@{mention_name}")
    user_ids.append(user_id)

  if mention_chunks:
    if text and not text.endswith(" "):
      text += " "

    mentions_start = len(text)
    mention_text = normalized_separator.join(mention_chunks)
    text += mention_text

    running_offset = mentions_start
    for chunk in mention_chunks:
      loci.append([running_offset, len(chunk)])
      running_offset += len(chunk) + len(normalized_separator)

  suffix = str(suffix_text or "")
  if suffix:
    if text and not text.endswith(" "):
      text += " "
    text += suffix

  attachments: list[Attachment] = []
  if user_ids and loci:
    attachments.append(mentions_attachment(user_ids=user_ids, loci=loci))

  return text.strip(), attachments


def sanitize_message_attachments(value: Any) -> list[Attachment]:
  raw_attachments: list[Any]
  if isinstance(value, dict):
    raw_attachments = [value]
  elif isinstance(value, list):
    raw_attachments = value
  else:
    return []

  sanitized: list[Attachment] = []
  for attachment in raw_attachments:
    if not isinstance(attachment, dict):
      continue

    attachment_type = str(attachment.get("type") or "").strip().lower()
    if attachment_type not in _SENDABLE_ATTACHMENT_TYPES:
      continue

    normalized = dict(attachment)
    normalized["type"] = attachment_type

    if attachment_type == "image":
      if not _non_empty_string(normalized.get("url")):
        continue
    elif attachment_type == "video":
      if not _non_empty_string(normalized.get("url")):
        continue
      if not _non_empty_string(normalized.get("preview_url")):
        continue
    elif attachment_type == "file":
      if not _non_empty_string(normalized.get("file_id")):
        continue
    elif attachment_type == "location":
      if not _non_empty_string(normalized.get("name")):
        continue
      if not _non_empty_string(normalized.get("lat")):
        continue
      if not _non_empty_string(normalized.get("lng")):
        continue
      normalized["lat"] = str(normalized["lat"])
      normalized["lng"] = str(normalized["lng"])
    elif attachment_type == "emoji":
      if not _non_empty_string(normalized.get("placeholder")):
        continue
      if not isinstance(normalized.get("charmap"), list):
        continue
    elif attachment_type == "reply":
      reply_id = normalized.get("reply_id")
      base_reply_id = normalized.get("base_reply_id")
      if not _non_empty_string(reply_id) and not _non_empty_string(base_reply_id):
        continue
      if not _non_empty_string(base_reply_id):
        normalized["base_reply_id"] = str(reply_id)
      if _non_empty_string(reply_id):
        normalized["reply_id"] = str(reply_id)
      normalized["base_reply_id"] = str(normalized["base_reply_id"])
    elif attachment_type == "mentions":
      user_ids = normalized.get("user_ids")
      loci = normalized.get("loci")
      if not isinstance(user_ids, list) or not isinstance(loci, list):
        continue
      if not user_ids or not loci or len(user_ids) != len(loci):
        continue
      normalized["user_ids"] = [str(item) for item in user_ids]

      normalized_loci: list[list[int]] = []
      valid_loci = True
      for entry in loci:
        if not isinstance(entry, list) or len(entry) != 2:
          valid_loci = False
          break
        try:
          start = int(entry[0])
          length = int(entry[1])
        except (TypeError, ValueError):
          valid_loci = False
          break
        if start < 0 or length <= 0:
          valid_loci = False
          break
        normalized_loci.append([start, length])

      if not valid_loci:
        continue
      normalized["loci"] = normalized_loci

    sanitized.append(normalized)

  return sanitized


def _non_empty_string(value: Any) -> bool:
  return value is not None and str(value).strip() != ""


__all__ = [
  "Attachment",
  "build_mentions_message",
  "emoji_attachment",
  "file_attachment",
  "image_attachment",
  "location_attachment",
  "mentions_attachment",
  "reply_attachment",
  "sanitize_message_attachments",
  "video_attachment",
]