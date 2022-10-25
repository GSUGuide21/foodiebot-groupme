import os
import re
import random

class Response:
	REGEX = re.compile(r"(.+)", re.MULTILINE)

	def __init__(self):
		print(f"Response loaded: {self.__class__.__name__}")

	def wave(self):
		return "👋" + random.choice("🏻🏼🏽🏾🏿")

	def respond(self, message, matches):
		pass