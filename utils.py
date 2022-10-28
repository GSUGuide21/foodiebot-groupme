import os
from enum import Enum
from datetime import datetime

def process_args(text: str | None, args_type="string") -> str | list[str]:
	match args_type:
		case "string":
			return str(text)
		case "list":
			return text.strip( ).split(" ")
		case "number":
			return int(text)

	return ""

class SenderType(Enum):
	User = "user"
	Bot = "bot"
	System = "system"

class Message:
	def __init__(self, raw={}, text=None):
		self.raw = raw or {"attachments": []}
		self.text = text or raw.get("text")
		self.user_id = raw.get("user_id")
		
		time = raw.get("created_at", datetime.now())
		
		if type(time) == int:
			self.time = datetime.fromtimestamp(time)
		else:
			self.time = time

		self.name = raw.get("name", "Test")
		self.sender_type = SenderType(raw.get("sender_type", "user"))
		self.group_id = raw.get("group_id")
		self.avatar_url = raw.get("avatar_url")
		print(self)

	def __repr__(self):
		return f'{self.group_id} | {self.name}: {self.text}'

	@property
	def image_url(self):
		attachments = [attachment for attachment in self.raw["attachments"] if attachment["type"] == "image"]
		if attachments:
			return attachments[0]["url"]
