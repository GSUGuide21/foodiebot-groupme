import re
import random
from .base import SystemCommand

class Removed(SystemCommand):
	REGEX = re.compile(r"(.+) removed (.+) from the group")
	RESPONSE_PATTERN = re.compile(r"%([^%]+)%")

	def __init__(self):
		super().__init__()
		with open("assets/text/removed.txt") as f:
			self.responses = f.readlines()

	def response(self, message, matches: list[str] | None):
		performer, target = matches

		data = { 
			"performer": performer,
			"target": target
		}

		result = random.choice(self.responses)

		def repl(match: re.Match):
			result = data[match.group(0)]
			return result or match.group(0)

		result = self.RESPONSE_PATTERN.sub(repl, result)
		return result