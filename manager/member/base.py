import os, time, requests
from manager import *
from util import urljoin

class Member(Manager):
	def __init__(self, user, group):
		super(Member, self).__init__(path="groups")
		self.group: Group = group
		self.access_token = self.group.access_token
		self.nick: str = user["nickname"]
		self.name: str = user["name"]
		self.id: str = user["id"]
		self.user_id: str = user["user_id"]
		self.roles: list[str] = user["roles"]
		self.muted: bool = user["muted"]
		self.avatar_url: str = user["image_url"]

	def __repr__(self):
		return f"{self.nick} ({self.user_id})"

	def has_role(self, role: str):
		return role in self.roles

	def has_roles(self, roles: list[str]):
		for role in roles:
			if not self.has_role(role):
				return False

		return True

	def kick(self):
		group_url = self.group.url
		member_url = urljoin(group_url, f"members/{self.id}")
		headers = { "X-Access-Token": self.access_token }
		response = requests.post(f"{member_url}/remove", data={}, headers=headers)