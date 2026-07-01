from __future__ import annotations

from typing import Any

from .base import Manager


class MeManager(Manager):
  def __init__(self, **options: Any):
    super().__init__(path="users/me", **options)

  def get_profile(self):
    headers = {"X-Access-Token": self.token}
    return self.GET(headers=headers).json().get("response")
