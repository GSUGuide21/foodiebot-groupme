import os, re, requests, time
from ..util import urljoin
from .base import Manager
from .member import Member

class Group(Manager):
	ACCESS_TOKEN = os.environ.get("access_token")

	def __init__(self, **options):
		super().__init__(path="/groups")
		self.group_id = options.get("group_id")
		self.owners: dict[str, Member] = {}
		self.coowners: dict[str, Member] = {}
		self.admins: dict[str, Member] = {}
		self.members: dict[str, Member] = {}

	def __repr__(self):
		return f"{self.name} ({self.group_id})"

	def __iter__(self):
		yield from self.members.values()

	def fetch(self):
		url = f"{urljoin(self.url, self.group_id)}?token={self.ACCESS_TOKEN}"
		response = requests.get(url).json()["response"]

		time.sleep(2)
		self.name = response["name"]
		self.message_count = response["messages"]["count"]
		self.creator_id = response["creator_user_id"]
		self.avatar_url = response["image_url"]
		self.description = response["description"]
		self.share_url = response["share_url"]
		self.requires_approval = response["requires_approval"] or False
		self.show_join_question = response["show_join_question"] or False
		self.join_question = response["join_question"] or None
		self.generate_users(response["members"])

		return self

	def generate_users(self, members):
		for member in members:
			self.members[member["user_id"]] = Member(member, self)
			if "owner" in self.members[member["user_id"]].roles:
				self.owner = self.members[member["user_id"]]
			if "admin" in self.members[member["user_id"]].roles:
				self.admins[member["user_id"]] = self.members[member["user_id"]]
	
	def find_admins(self):
		admins = []

		for member in self.members.values():
			if member.is_admin:
				admins.append(member)

		return member

	def find_member(self, user_id):
		for member in self.members.values():
			if member.user_id == user_id:
				return member

		return None

	def find_members(self, user_ids: list):
		members = []
		for user_id in user_ids:
			member = self.find_member(user_id)
			if member is not None:
				members.append(member)
		
		return members

	def find_member_by_name(self, nick: str):
		for member in self.members.values():
			if member.nick == nick:
				return member
		
		return None

	def find_members_by_name(self, nicks: list[str]):
		members = []
		for nick in nicks:
			member = self.find_member_by_name(nick)
			if member is not None:
				members.append(member)

		return members
