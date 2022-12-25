from commands.base import Command
from random import getrandbits

class Capitalize(Command):
	min_arguments = 1
	description = "Scrambles the text"
	category = "Fun"
	
	def scramble(self, string):
		capitalize = bool(getrandbits(1))
		return string.capitalize() if capitalize else string.lower()

	def respond(self, **options):
		result = options.get("result")
		return str.join("", [self.scramble(c) for c in result])

def load():
	return Capitalize()