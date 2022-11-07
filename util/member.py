import os, time, requests

class Member:
	def __init__(self, user, group):
		self.group = group
		self.nick: str = user["nickname"]
		self.name: str = user["name"]
		self.user_id: str = user["user_id"]
		self.roles: list[str] = user["roles"]
		self.muted: bool = user["muted"]
		self.avatar_url: str = user["image_url"]

		self.is_owner = "owner" in self.roles
		self.is_admin = "admin" in self.roles
		self.is_creator = group.creator_id == self.user_id
