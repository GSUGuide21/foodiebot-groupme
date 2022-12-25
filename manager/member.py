import requests
from manager import *
from util import urljoin, RoleType

class Member(Manager):
	def __init__(self, **options):
		super(Member, self).__init__(path="groups")
		raw = options.get("user", options.get("member"))

		self.group = options.get("group")
		self.access_token = self.group.access_token
		self.raw = raw
		self.state = {}

		self.nick: str = raw["nickname"]
		self.name: str = raw["name"]
		self.id: str | int = raw["id"]
		self.user_id: str = raw["user_id"]
		self.roles: list[str] = raw["roles"]
		self.muted: bool = raw["muted"]
		self.avatar_url: str = raw["image_url"]

		self.url = f"{self.url}/{self.group.id}/members/{self.id}/remove"

	def __eq__(self, other):
		return self.id == other.id
	
	@property
	def is_owner(self):
		return RoleType.Owner in self.roles

	@property
	def is_admin(self):
		return RoleType.Admin in self.roles

	def kick(self):
		headers = {"X-Access_Token": self.access_token}
		response = self.post(headers=headers).json()["response"]
		return response