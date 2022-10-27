import os
import re
import random
from .base import Response

class Say(Response):
	def __init__(self):
		super().__init__()
		with open("assets/triggers/say.txt") as f:
			parts = [line for line in f.readlines() if line != ""]
			parts = [self.preprocess(line) for line in parts if line != ""]
			self.REGEX = re.compile(fr"{str.join('|', parts)}", flags=re.IGNORECASE | re.MULTILINE)

		with open("assets/text/say.txt") as g:
			self.responses = g.readlines()

	def preprocess(self, string):
		return string