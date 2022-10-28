import os
import re
import requests
from .base import Command
from bs4 import BeautifulSoup, ResultSet, Tag
from selenium import webdriver
from ...utils import DRIVER

CAMPUS_LABS_URL = "https://gsu.campuslabs.com/engage/events?perks=FreeFood"

class Test(Command):
	EVENT_ID_PATTERN = re.compile(r"(?:https:\/\/gsu\.campuslabs\.com|)\/engage\/event\/(\d+)", flags=re.IGNORECASE)

	def __init__(self):
		DRIVER.get(CAMPUS_LABS_URL)
		request = requests.get(DRIVER.page_source)
		content = request.content

		soup = BeautifulSoup(content, features="html5lib")
		body = soup.body

		print(body)
		"""
		result = []

		for div in divs:
			result.append(self.parse_event(div))

		self.results = result
		self.limit = 10
		"""

	def parse_event(self, div: Tag):
		child = div.find("a", recursive=False)
		link = child.get("href")
		root = child.select_one(".MuiCard-root")
		title = child.select_one(".MuiPaper-root h3")
		title_text = title.get_text().strip()

		if re.match(self.EVENT_ID_PATTERN, link):
			match: re.Match[str] = re.match(self.EVENT_ID_PATTERN, link)
			event_id = match.group()
		else:
			event_id = None

		info = root.select_one("div:nth-child(3)")
		
		datetime = info.select_one("div:first-child")
		location = info.select_one("div:last-child")

		datetime = datetime.get_text().strip()
		location = location.get_text().strip()

		data = {
			"link": link,
			"event_id": event_id or "No event ID available",
			"title": title_text,
			"datetime": datetime,
			"location": location
		}

		return data

	def handle_args(self, query: str | None):
		if query is None or query != "":
			return self.limit

		results = [result for result in self.spaces(query)]
		limit = int(results[0] if len(results) > 0 and results[0] > 0 else self.limit)
		return limit

	def response(self, query, message, bot_id, app_id):
		print(len(self.results))
		limit = self.handle_args(query)
		result = self.results[0:limit]
		return "Events found on PIN: \n{event_list}".format(event_list=str.join("\n", result))
