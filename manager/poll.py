import os
import requests

from time import sleep
from manager.base import Manager
from manager.member import Member

class PollManager(Manager):
	def __init__(self, **options):
		super(PollManager, self).__init__(path="poll")
		self.access_token = os.environ.get("access_token")
		self.group_id = options.get("group_id")
		self.url = f"{self.url}/{self.group_id}"

	def get_polls(self):
		headers = {"X-Access-Token": self.access_token}
		response = self.get(headers=headers).json()["response"]
		polls = [Poll(**poll) for poll in response["polls"]]
		return polls

class Poll:
	def __init__(self, **options):
		self.raw = options

		self.data = options.get("data", {})
		self.id = self.data.get("id")
		self.subject = self.data.get("subject")
		self.owner = Member(id=self.data.get("owner_id"))
		self.created = self.data.get("created_at")
		self.expiry = self.data.get("expiration")
		self.status = self.data.get("status")
		self.last_modified = self.data.get("last_modified")
		self.type = self.data.get("type", "single")
		self.visibility = self.data.get("visibility", "anonymous")
		
		self.user_votes = options.get("user_votes", [])
		self.user_vote = options.get("user_vote", None)

	@staticmethod
	def get_from_id(**options):
		id = options.get("id", "")
		group_id = options.get("group", {})["id"] or ""
		if group_id == "" or id == "": return None

		url = f"https://api.groupme.com/v3/poll/{group_id}/{id}"
		headers = {"X-Access-Token": os.environ.get("access_token")}
		response = requests.get(url, headers=headers).json()["response"]
		sleep(3)

		return Poll(**response)

	@property
	def total(self):
		poll_options = self.data.get("options", [])
		votes = [option["votes"] for option in poll_options if option["votes"] is not None]
		votes = [int(vote) for vote in votes]
		return sum(votes)

	@property
	def options(self):
		poll_options = self.data.get("options", [])

		result = []
		for option in poll_options:
			if option is None: continue
			option["poll"] = self
			result.append(PollOption(**option))

		return result

class PollOption:
	def __init__(self, **options):
		self.raw = options

		self.id = options.get("id")
		self.title = options.get("title")
		self.votes = int(options.get("votes", 0))
		self.poll = options.get("poll")

		self.percentage = self.votes / self.poll.total
		
	@property
	def voters(self):
		voter_ids = self.raw.get("voter_ids", [])
		result = [Member(id=id) for id in voter_ids]
		return result