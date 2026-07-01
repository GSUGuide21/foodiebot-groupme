from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from client.commands.result import CommandResultLike

if TYPE_CHECKING:
	from client.commands import CommandContext
	from client.parser import ParsedMessage
	from client.preconditions.base import Precondition

class Command(ABC):
	name: str = ""
	aliases: list[str] = []
	preconditions: list[Precondition] = []
	description: str = ""
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
			preconditions=self.preconditions,
			aliases=self.aliases,
			timeout_seconds=self.timeout_seconds,
		)

	def handle(self, message: ParsedMessage, context: CommandContext) -> CommandResultLike:
		return self.execute(message, context)

	@abstractmethod
	def execute(self, message: ParsedMessage, context: CommandContext) -> CommandResultLike:
		raise NotImplementedError