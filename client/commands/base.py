from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from client.commands.result import CommandResultLike

if TYPE_CHECKING:
	from client.commands import CommandContext
	from client.parser import ParsedMessage
	from client.preconditions.base import Precondition
	from client.manager import Group

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

	def resolve_members_from_mentions(self, raw: dict[str, object] | None, group: Group):
		if not isinstance(raw, dict):
			return []

		attachments = raw.get("attachments")
		if not isinstance(attachments, list):
			return []

		mentioned_user_ids: list[str] = []
		seen_user_ids: set[str] = set()

		for attachment in attachments:
			if not isinstance(attachment, dict) or attachment.get("type") != "mentions":
				continue

			user_ids = attachment.get("user_ids")
			if not isinstance(user_ids, list):
				continue

			for user_id in user_ids:
				normalized_user_id = str(user_id or "").strip()
				if not normalized_user_id or normalized_user_id in seen_user_ids:
					continue

				seen_user_ids.add(normalized_user_id)
				mentioned_user_ids.append(normalized_user_id)

		if not mentioned_user_ids:
			return []

		members_by_user_id: dict[str, dict[str, Any]] = {}
		for member in group.get_members():
			member_user_id = str(member.get("user_id") or "").strip()
			if not member_user_id:
				continue
			members_by_user_id[member_user_id] = member

		resolved_members: list[dict[str, Any]] = []
		for user_id in mentioned_user_ids:
			member = members_by_user_id.get(user_id)
			if member is not None:
				resolved_members.append(member)

		return resolved_members

	def resolve_members_from_mention(self, raw: dict[str, object] | None, group: Group):
		return self.resolve_members_from_mentions(raw, group)

	def handle(self, message: ParsedMessage, context: CommandContext) -> CommandResultLike:
		return self.execute(message, context)

	@abstractmethod
	def execute(self, message: ParsedMessage, context: CommandContext) -> CommandResultLike:
		raise NotImplementedError