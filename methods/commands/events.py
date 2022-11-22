import os, re, requests
from .base import Command
from manager import EventManager
from bs4 import BeautifulSoup, ResultSet, Tag
from time import sleep
from ..driver import driver

class Events(Command):
	DESCRIPTION = "Posts a list of events to the group chat!"
	EVENT_ID_PATTERN = re.compile(r"\/engage\/event\/(\d+)", flags=re.IGNORECASE)
	SEPARATOR_PATTERN = re.compile(r"([^=]+)=(.*)", flags=re.MULTILINE)
	COMMA_PATTERN = re.compile(r"\s*,\s*", flags=re.MULTILINE)
	CATEGORY = "Event"
	ARGUMENT_TYPE = "semicolon"

	CATEGORIES = {
		"ATL": 8776,
		"ALP": 8775,
		"CLK": 8777,
		"DEC": 8778,
		"DUN": 8779,
		"NWT": 8780
	}

	CATEGORY_ALIASES = {
		"ATL": ["Atlanta Campus", "Atlanta"],
		"ALP": ["Alpharetta Campus", "Alpharetta"],
		"CLK": ["Clarkston Campus", "Clarkston"],
		"DEC": ["Decatur Campus", "Decatur"],
		"DUN": ["Dunwoody Campus", "Dunwoody"],
		"NWT": ["Newton Campus", "Newton"]
	}

	def __init__(self, **options):
		self.limit = options.get("limit", 3)
		self.min = options.get("min", 1)
		self.max = options.get("max", 8)
		self.event_manager = EventManager()

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
			event["link"] = "{path}/{id}".format(path=self.CAMPUS_LABS_EVENT_PATH,id=event["event_id"])
			result = "{title}\nLocation: {location}\nDate and Time: {datetime}\nLink: {link}".format(**event)

			results.append(result)

		return str.join("\n", results)

	def clamp(self, n: int | float):
		return max(self.min, min(n, self.max))

	def get_category_id(self, category):
		if category.upper() in self.CATEGORIES:
			return self.CATEGORIES[category.upper()]

		for category_key, aliases in self.CATEGORY_ALIASES.items():
			if category in aliases:
				return self.CATEGORY[category_key]

	def respond(self, **options):
		query = options.get("query", "")
		args = self.parse_arguments(query=query)
		params = {}
		
		for item in args.result:
			if re.match(self.SEPARATOR_PATTERN, item):
				match = re.findall(self.SEPARATOR_PATTERN, item)
				key, value = match
				params[key] = value

		perks = params.get("perks", "FreeFood")
		perks = re.split(self.COMMA_PATTERN, perks)

		categories = params.get("categories", "ATL")
		categories = re.split(self.COMMA_PATTERN, categories)

		url = f"{self.event_manager.url}?perks={str.join('&perks=', perks)}"

		if categories != "":
			url = f"{url}&categories={str.join('&categories=', categories)}"

		driver.get(url)
		sleep(3)

		limit = int(params.get('limit', self.limit))
		limit = self.clamp(limit)

		results = self.generate_events(driver.page_source)
		results = results[0:limit]
		driver.close()

		opts = {
			"plural": "s" if len(results) != 1 else "",
			"event_list": self.parse_event_string(results)
		}

		return "Event{plural} found on PIN: \n{event_list}".format(**opts)