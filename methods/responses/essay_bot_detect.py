import os
import re
import random
from .base import Response


class EssayBotDetect(Response):
	REGEX = re.compile(r"https?\://(?:e?x(?:tra|)essay(?:[sz]|service|)|paper(?:ok|c|z|s|g))\.(?:cf|ml|ga|gq)", flags=re.MULTILINE | re.IGNORECASE)
	USERNAME_REGEX = re.compile(r"%USER(?:NAME|)%", flags=re.IGNORECASE | re.MULTILINE)

	def __init__(self):
		super().__init__()
		with open("assets/text/essaybot.txt") as f:
			self.responses = f.readlines()	

	def respond(self, message, matches: list[str] | None):
		result = random.choice(self.responses)
		name = message.name

		result = self.USERNAME_REGEX.sub(name, result)
		return result