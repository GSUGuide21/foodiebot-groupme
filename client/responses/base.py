from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import re

from client.responses.result import ResponseResultLike

if TYPE_CHECKING:
  from client.responses import ResponseContext
  from client.parser import ParsedMessage

class Response(ABC):
  name: str = ""
  targets: list[str | re.Pattern] = []
  triggers: list[str] = []
  description: str = ""
  priority: int = 0
  timeout_seconds: float | None = None

  @classmethod
  def create(cls, router):
    return cls()

  def register(self, router) -> None:
    handler = self.handle
    router.register(
      self.name,
      handler,
      description=self.description,
      targets=self.targets,
      triggers=self.triggers,
      priority=self.priority,
      timeout_seconds=self.timeout_seconds,
    )

  def handle(self, message: ParsedMessage, context: ResponseContext) -> ResponseResultLike:
    return self.execute(message, context)

  @abstractmethod
  def execute(self, message: ParsedMessage, context: ResponseContext) -> ResponseResultLike:
      raise NotImplementedError