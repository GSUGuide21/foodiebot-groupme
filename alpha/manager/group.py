import os
import requests
from time import sleep
from alpha.util import RoleType
from .base import Manager
from .member import Member
from .poll import PollManager

class Group(Manager):
	def __init__(self, **options):
		super(Group, self).__init__(path=f"groups/{options.get('group_id')}")
		
		self.access_token = os.environ.get("access_token")
		self.group_id = options.get("group_id")
		self.owner = None
		self.admins: dict[str, Member] = {}
		self.members: dict[str, Member] = {}
		self.polls = PollManager(group_id=self.group_id)

	def __repr__(self):
		return f"{self.name} ({self.group_id})"

	def __iter__(self):
		yield from self.members.values()

	def fetch(self):
		headers = {"X-Access-Token": self.access_token}
		response = requests.get(self.url, headers=headers).json()["response"]
		sleep(3)

		self.name = response["name"]
		self.messages = response["messages"]
		self.last_message_id = self.messages["last_message_id"]
		self.message_count = self.messages["count"]
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
			self.members[member["user_id"]] = Member(member=member, group=self)
			if RoleType.Owner in self.members[member["user_id"]].roles:
				self.owner = self.members[member["user_id"]]
			elif RoleType.Admin in self.members[member["user_id"]].roles:
				self.admins[member["user_id"]] = self.members[member["user_id"]]

	def find(self, callback, list_or_tuple):
		if not callable(callback): return ValueError("Callback must be callable")
		items = list(list_or_tuple)

		for value in items:
			if callback(value): return value

		return None

	def find_member(self, user_id):
		return self.find(lambda member: member["user_id"] == user_id, self.members.values())

	def find_members(self, user_ids: list):
		members = [self.find_member(user_id) for user_id in user_ids]
		return [member for member in members if member != None]

	def find_member_by_name(self, nick):
		return self.find(lambda member: member["nick"] == nick, self.members.values())