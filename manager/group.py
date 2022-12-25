import os, requests
from time import sleep
from util import RoleType
from manager import *

class Group(Manager):
	def __init__(self, **options):
		super(Group, self).__init__(path="groups")

		self.access_token = os.environ.get("access_token")
		self.group_id = options.get("group_id")

		self.url = f"{self.url}/{self.group_id}"

		self.owner = None
		self.admins: dict[str, Member] = {}
		self.members: dict[str, Member] = {}

		self.poll_manager = PollManager(group_id=self.group_id)
		self.calendar_manager = CalendarManager(group_id=self.group_id)

	def get_messages(self):
		headers = {"X-Access-Token": self.access_token}
		response = requests.get(f"{self.url}/messages", headers=headers).json()["response"]
		return [Message(message) for message in response["messages"]]

	def get_events(self):
		return self.calendar_manager.get_events()

	def get_polls(self):
		return self.poll_manager.get_polls()