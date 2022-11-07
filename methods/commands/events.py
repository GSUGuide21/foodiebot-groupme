import os, re, requests
from .base import Command
from bs4 import BeautifulSoup, ResultSet, Tag
from time import sleep
from ..driver import driver

class Events(Command):
	CAMPUS_LABS_URL = "https://gsu.campuslabs.com/engage/events?perks=FreeFood"
	CAMPUS_LABS_EVENT_PATH = "https://gsu.campuslabs.com/engage/event"
	DESCRIPTION = "Posts a list of events to the chat"
	EVENT_ID_PATTERN = re.compile(r"\/engage\/event\/(\d+)", flags=re.IGNORECASE)
	CATEGORY = "Event"
	ARGUMENT_TYPE = "spaces"

	def __init__(self, **options):
		self.limit = options.get("limit", 3)
		self.min = options.get("min", 1)
		self.max = options.get("max", 7)

	def generate_events(self, source):
		soup = BeautifulSoup(source, features="html5lib")
		root = soup.find("div", id="event-discovery-list")
		elements = root.div.find_all("div", recursive=False)

		results = [self.parse_event(div) for div in elements]
		return results

	def parse_event(self, element):
		child = element.find("a", recursive=False)
		link: str = child.get("href")
		root = child.select_one(".MuiCard-root")
		title = child.select_one(".MuiPaper-root h3")
		title_text: str = title.get_text().strip()

		if re.match(self.EVENT_ID_PATTERN, link):
			match: re.Match[str] = re.match(self.EVENT_ID_PATTERN, link)
			event_id: str = match.group(1)
		else:
			event_id = None

		info = root.select_one("div:nth-child(3)")
		
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
				link="{path}/{id}".format(path=self.CAMPUS_LABS_EVENT_PATH,id=event["event_id"])
			)

			results.append(result)

		return str.join("\n", results)

	def clamp(self, n: int | float):
		return max(self.min, min(n, self.max))

	def respond(self, **options):
		driver.get(self.CAMPUS_LABS_URL)
		sleep(3)

		limit = self.parse_arguments(options.get("query", ""))
		limit: list = limit.result

		if not len(limit):
			limit = self.limit
		else:
			limit = self.clamp(int(limit[0]))

		results = self.generate_events(driver.page_source)
		results = results[0:limit]
		driver.close()

		return "Event{plural} found on PIN: \n{event_list}".format(
			plural="s" if len(results) != 1 else "",
			event_list=self.parse_event_string(results)
		)