import os
import re
import random
from .base import Response

class Hello(Response):
	REGEX = re.compile(r"(?:H(?:e(?:y|llo)|i)|W(?:hat\'s up|assup)) FoodieBot!?", flags=re.IGNORECASE)
	USERNAME_REGEX = re.compile(r"%USER(?:NAME|)%", flags=re.IGNORECASE | re.MULTILINE)
	WAVE_PATTERN = re.compile(r"%WAVE%", flags=re.IGNORECASE | re.MULTILINE)

	def __init__(self):
		super().__init__()
		with open("assets/text/hello.txt") as f:
			self.responses = f.readlines()

	def respond(self, message, matches: list[str] | None):
		result = random.choice(self.responses)
		result = self.WAVE_PATTERN.sub(self.wave(), result)
		result = self.USERNAME_REGEX.sub(message.name, result)

