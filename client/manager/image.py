from __future__ import annotations

from typing import Any

from .base import Manager


class ImageManager(Manager):
  base_url = "https://image.groupme.com/pictures"

  def __init__(self, **options: Any):
    super().__init__(path="", **options)

  def upload(self, content_type: str, data: bytes):
    headers = {
      "X-Access-Token": self.token,
      "Content-Type": content_type,
    }
    return self.POST(headers=headers, data=data)
