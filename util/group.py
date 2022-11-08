import os, re, requests
from time import sleep
from .member import Member

class Group:
	# Constants
	API_ENDPOINT = "https://api.groupme.com/v3/groups"
	ACCESS_TOKEN = os.environ.get("access_token")

	def __init__(self, group_id):
		self.group_id = group_id
		self.members: dict[str, Member] = {}
		self.owner = None
		self.admins: dict[str, Member] = {}

	def __repr__(self):
		return f"{self.name} ({self.group_id})"

	def fetch(self):
		response = requests.get(f"{self.API_ENDPOINT}/{self.group_id}?token={self.ACCESS_TOKEN}").json()["response"]

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
			if "owner" in self.members[member["user_id"]].roles:
				self.owner = self.members[member["user_id"]]
				continue
			if "admin" in self.members[member["user_id"]].roles:
				self.admins[member["user_id"]] = self.members[member["user_id"]]

	def find_member(self, user_id):
		for member in self.members.values():
			if member.user_id == user_id:
				return member
		return None

	def get_owner(self):
		for member in self.members.values():
			if member.is_owner:
				return member

		return None

	def get_admins(self):
		admins = []
		for member in self.members.values():
			if member.is_admin:
				admins.append(member)

		return admins

	def get_member_by_name(self, nick: str):
		for member in self.members.values():
			if member.nick == nick:
				return member
			
		return None

	def get_members_by_names(self, nicks: list[str]):
		members = [self.get_member_by_name(nick) for nick in nicks]
		return members