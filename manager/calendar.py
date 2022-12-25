import os
import requests

from time import sleep
from beta.manager.base import Manager
from beta.manager.event import Event

class CalendarManager(Manager):
	def __init__(self, **options):
		super(CalendarManager, self).__init__(path="conversations")
		self.access_token = os.environ.get("access_token")
		self.group_id = options.get("group_id")
		self.url = f"{self.url}/{self.group_id}/events/list"

	def get_events(self):
		headers = {"X-Access-Token": self.access_token}
		response = self.get(headers=headers).json()["response"]
		sleep(3)

		events = response.get("events", [])
		events = [Event(**event) for event in events]
		return events