import os
import re
import random
from util import preconditions

class Response:
	PRECONDITIONS = []

	def __init__(self):
		print(f"Response ({self.__class__.__name__}) loaded!")
	
	def wave(self):
		return "👋" + random.choice("🏻🏼🏽🏾🏿")

	def validate(self, **options):
		pass

	def respond(self, **options):
		pass

"""
class Response:
	REGEX = re.compile(r"(.+)", re.MULTILINE)
	USERNAME_REGEX = re.compile(r"%USER(?:NAME|)%", flags=re.IGNORECASE | re.MULTILINE)
	WAVE_PATTERN = re.compile(r"%WAVE%", flags=re.IGNORECASE | re.MULTILINE)

	def __init__(self):
		print(f"Response loaded: {self.__class__.__name__}")

	def wave(self):
		return "👋" + random.choice("🏻🏼🏽🏾🏿")

	def matches(self, query: str | None) -> bool:
		if self.triggers == None:
			return re.match(self.REGEX) != None
		else:
			triggers = [trigger.lower() for trigger in self.triggers if trigger != ""]
			return query.lower() in triggers

	def respond(self, message, matches):
		pass
"""