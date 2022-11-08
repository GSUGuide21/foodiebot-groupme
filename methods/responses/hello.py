import os
import re
import random
from .base import Response

class Hello(Response):
	#REGEX = re.compile(r"(?:H(?:e(?:y|llo)|i)|W(?:hat\'s up|assup)) FoodieBot!?", flags=re.IGNORECASE)

	def __init__(self):
		super().__init__()
		with open("assets/triggers/hello.txt") as f:
			parts = [line for line in f.readlines() if line != ""]
			print(parts)
			self.REGEX = re.compile(fr"{str.join('|', parts)}", flags=re.IGNORECASE | re.MULTILINE)

		with open("assets/text/hello.txt") as g:
			self.responses = g.readlines()

	def respond(self, message, matches: list[str] | None):
		result = random.choice(self.responses)
		result = self.WAVE_PATTERN.sub(self.wave(), result)
		result = self.USERNAME_REGEX.sub(message.name, result)
		return result