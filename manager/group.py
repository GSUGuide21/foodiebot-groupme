import os, re, requests
from time import sleep
from .base import *
from .member import *

class Group(Manager):
	def __init__(self, **options):
		super(Group, self).__init__(path=f"/groups/{options.get('group_id')}")
		self.access_token = os.environ.get("access_token")
		self.group_id = options.get("group_id")

		self.members: dict[str, Member] = {}
		self.coowners: dict[str, Member] = {}
		self.admins: dict[str, Member] = {}
		self.owner = None

	def __repr__(self):
		return f"{self.name} ({self.group_id})"

	def __iter__(self):
		yield from self.members.values()

	def fetch(self):
		print(self.url)
		response = requests.get(f"{self.url}?token={self.access_token}").json()["response"]

		sleep(2)
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
			if "owner" in self.member[member["user_id"]].roles:
				self.owner = self.members[member["user_id"]]
			elif "admin" in self.member[member["user_id"]].roles:
				self.admins[member["user_id"]] = self.members[member["user_id"]]

	def find_member(self, user_id):
		for member in self.members.values():
			if member["user_id"] == user_id:
				return member

		return None

	def find_members(self, user_ids: list):
		members = []
		for user_id in user_ids:
			member = self.find_member(user_id)
			if member is not None:
				members.append(member)
		
		return members

	def find_members_by_name(self, nick: str):
		for member in self.members.values():
			if member.nick == nick:
				return member
		
		return None	