import os
import re
import requests
from .base import Command
from bs4 import BeautifulSoup, ResultSet, Tag
from selenium import webdriver
from ..driver import DRIVER

CAMPUS_LABS_URL = "https://gsu.campuslabs.com/engage/events?perks=FreeFood"
CAMPUS_LABS_EVENT_PATH = "https://gsu.campuslabs.com/engage/event"

class Events(Command):
	DESCRIPTION = "Posts a list of events to the chat"
	EVENT_ID_PATTERN = re.compile(r"\/engage\/event\/(\d+)", flags=re.IGNORECASE)

	def __init__(self):
		super().__init__()
		self.limit = 3
		self.min = 1
		self.max = 6

	def fetch_events(self):
		DRIVER.get(CAMPUS_LABS_URL)
		content = DRIVER.page_source

		soup = BeautifulSoup(content, features="html5lib")
		root = soup.find("div", id="event-discovery-list")
		divs = root.div.find_all("div", recursive=False)

		results = []

		for div in divs:
			results.append(self.parse_event(div))

		return results

	def parse_event(self, div: Tag):
		child = div.find("a", recursive=False)
		link: str = child.get("href")
		root = child.select_one(".MuiCard-root")
		title = child.select_one(".MuiPaper-root h3")
		title_text: str = title.get_text().strip()

		if re.match(self.EVENT_ID_PATTERN, link):
			match: re.Match[str] = re.match(self.EVENT_ID_PATTERN, link)
			event_id: str = match.group(1)
		else:
			event_id = None

		info = root.select_on.e("div:nth-child(3)")
		
		datetime = info.div.select_one("div:first-child")
		location = info.div.select_one("div:last-child")

		datetime: str = datetime.get_text().strip()
		location: str = location.get_text().strip()

		data = {
			"link": link,
			"event_id": event_id or "No event ID available",
			"title": title_text,
			"datetime": datetime,
			"location": location
		}

		return data

	def parse_event_string(self, events: list[dict[str, str]]):
		results = []

		for event in events:
			result = "{title}\nLocation: {location}\nDate and Time: {datetime}\nLink: {link}".format(
				location=event["location"],
				title=event["title"],
				datetime=event["datetime"],
				link="{path}/{id}".format(path=CAMPUS_LABS_EVENT_PATH,id=event["event_id"])
			)

			results.append(result)

		return str.join("\n", results)

	def clamp(self, n: int | float):
		return max(self.min, min(n, self.max))

	def handle_args(self, query: str | None):
		if query is None or query != "":
			return self.limit

		results = [result for result in self.spaces(query)]
		print(results)
		limit = int(results[0] if len(results) > 0 and results[0] > 0 else self.limit)
		limit: int = self.clamp(limit)

		return limit

	def response(self, query, message, bot_id, app_id):
		found_events = self.fetch_events()
		print(len(found_events))
		limit = self.handle_args(query)
		print(limit)
		results = found_events[0:limit]
		result = self.parse_event_string(results)
		return "Event{plural} found on PIN: \n{event_list}".format(
			plural="s" if len(results) != 1 else "",
			event_list=result
		)
