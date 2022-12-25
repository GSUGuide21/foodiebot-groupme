import re
from commands.base import Command
from bs4 import BeautifulSoup
from time import sleep
from manager.driver import Driver

driver = Driver().load()

class Events(Command):
	description = "Posts a list of events to the group chat!"
	category = "Event"
	argument_type = "semicolon"
	aliases = ["pin"]
	
	event_id_pattern = re.compile(r"\/engage\/event\/(\d+)", flags=re.IGNORECASE | re.MULTILINE)
	separator_pattern = re.compile(r"([^=]+)=(.*)", flags=re.MULTILINE)
	comma_pattern = re.compile(r"\s*,\s", flags=re.MULTILINE)
	event_path = "https://gsu.campuslabs.com/engage/event"
	events_path = "https://gsu.campuslabs.com/engage/events"

	categories = {
		"ATL": 8776,
		"ALP": 8775,
		"CLK": 8777,
		"DEC": 8778,
		"DUN": 8779,
		"NWT": 8780
	}

	category_aliases = {
		"ATL": ["Atlanta Campus", "Atlanta"],
		"ALP": ["Alpharetta Campus", "Alpharetta"],
		"CLK": ["Clarkston Campus", "Clarkston"],
		"DEC": ["Decatur Campus", "Decatur"],
		"DUN": ["Dunwoody Campus", "Dunwoody"],
		"NWT": ["Newton Campus", "Newton"]
	}

	defaults = {
		"limit": 3,
		"min": 1,
		"max": 8
	}

	def generate_events(self, source):
		soup = BeautifulSoup(source, features="html5lib")
		root = soup.find("div", id="event-discovery-list")
		elements = root.div.find_all("div", recursive=False)
		return [self.parse_event(el) for el in elements]

	def parse_event(self, el):
		child = el.find("a", recursive=False)
		link = child.get("href")
		root = child.select_one(".MuiCard-root")
		title = child.select_one(".MuiPaper-root h3")
		title_text = title.get_text().strip()

		if re.match(self.event_id_pattern, link):
			m  = re.match(self.event_id_pattern, link)
			event_id = m.group(1)
		else: event_id = None

		info = root.select_one("div:nth-child(3)")

		datetime = info.div.select_one("div:first-child")
		location = info.div.select_one("div:last-child")

		datetime = datetime.get_text().strip()
		location = location.get_text().strip()

		data = {
			"link": link,
			"event_id": event_id or "No event ID available!",
			"title": title_text,
			"datetime": datetime,
			"location": location
		}

		return data

	def parse_event_string(self, events):
		results = []

		for event in events:
			event["link"] = "{path}/{id}".format(path=self.event_path, id=event["event_id"])
			result = "{title}\nLocation: {location}\nDate and Time: {datetime}\nLink: {link}".format(**event)
			results.append(result)

		return str.join("\n", results)

	def clamp(self, n: int | float, bounds = {}):
		return max(bounds.min, min(n, bounds.max))
	
	def get_category_id(self, category):
		if category.upper() in self.CATEGORIES:
			return self.CATEGORIES[category.upper()]

		for category_key, aliases in self.CATEGORY_ALIASES.items():
			if category in aliases:
				return self.CATEGORY[category_key]

	def respond(self, **options):
		args = options.get("args")
		params = {key: value for key, value in args.kwargs.items()}

		perks = params.get("perks", "FreeFood")
		perks = re.split(self.comma_pattern, perks)

		categories = params.get("categories", "ATL")
		categories = re.split(self.comma_pattern, categories)

		url = self.events_path
		query_set = False

		if len(perks) > 0:
			query_set = True
			url = f"{url}?perks={str.join('&perks=', perks)}"
		
		if len(categories) > 0:
			url = f"{url}{'&' if query_set else '?'}categories={str.join('&categories=', categories)}"

		driver.get(url)
		sleep(3)

		bounds = {}
		bounds["min"] = int(params.get("min", self.defaults["min"]))
		bounds["max"] = int(params.get("max", self.defaults["max"]))

		limit = int(params.get("limit", self.defaults["limit"]))
		limit = self.clamp(limit, bounds=bounds)

		results = self.generate_events(driver.page_source)
		results = results[0:limit]
		driver.close()

		opts = {
			"plural": "s" if len(results) != 1 else "",
			"event_list": self.parse_event_string(results)
		}

		return "Event{plural} found on PIN: \n{event_list}".format(**opts)

def load():
	return Events()