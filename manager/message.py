from datetime import datetime
from util.sendertype import SenderType
from manager.member import Member
from manager.group import Group

class Message:
	def __init__(self, raw={}, text=None):
		self.raw = raw or {"attachments": []}
		self.text: str = text or raw.get("text")
		self.user_id: str | int = raw.get("user_id")
		self.name: str = raw.get("name")
		self.sender_type = SenderType(raw.get("sender_type", "user"))
		self.group_id: str | int = raw.get("group_id")
		self.avatar_url: str = raw.get("avatar_url")

		time = raw.get("created_at", datetime.now())

		if type(time) == int: self.time = datetime.fromtimestamp(time)
		else: self.time = time

	def __repr__(self):
		return f"({self.group_id}) {self.name}: {self.text}"

	def __getitem__(self, key):
		return getattr(self, key)
	
	def __setitem__(self, key, value):
		return setattr(self, key, value)

	@property
	def group(self):
		return Group(self.group_id)

	@property
	def sender(self):
		return Member(self.user_id)

	@property
	def image_url(self):
		attachments = [attachment for attachment in self.raw["attachments"] if attachment["type"] == "image"]
		if attachments and len(attachments) > 0:
			return attachments.pop(0)["url"]

	@property
	def mentions(self):
		attachments = [attachment for attachment in self.raw["attachments"] if attachment["type"] == "mentions"]
		if attachments and len(attachments) > 0:
			mentions = attachments.pop(0)
			user_ids = mentions["user_ids"]
			loci = mentions["loci"]

			return {"user_ids": user_ids, "loci": loci}

	@property
	def reply(self):
		attachments = [attachment for attachment in self.raw["attachments"] if attachment["type"] == "reply"]
		if attachments and len(attachments) > 0:
			return attachments[0]["reply_id"]