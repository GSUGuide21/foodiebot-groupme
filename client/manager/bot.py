from __future__ import annotations

from .base import Manager


class BotManager(Manager):
  def __init__(self, **options):
    super().__init__(path="bots", **options)