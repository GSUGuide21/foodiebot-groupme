from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  ...

class Precondition(ABC):
  name: str = ""
  description: str = ""
  priority: int = 0

  @classmethod
  def create(cls, router):
    return cls()

  def register(self, router) -> None:
    handler = self.handle
    router.register_precondition(
      self.name,
      handler,
      description=self.description,
      priority=self.priority,
    )

  def handle(self, message, context) -> tuple[bool, str]:
    return self.execute(message, context)

  @abstractmethod
  def execute(self, message, context) -> tuple[bool, str]:
    raise NotImplementedError