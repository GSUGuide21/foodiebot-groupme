import re
import random
from responses.base import Response

class Hello(Response):
	def __init__(self):
		super(Hello, self).__init__()

		with open("assets/triggers/hello.txt") as f:
			parts = [line for line in f.readlines() if line != ""]
			self.triggers = parts

		with open("assets/responses/hello.txt") as g:
			self.responses = [line for line in g.readlines() if line != ""]

	def respond(self, **options):
		message = options.get("message")
		result = random.choice(self.responses)

		replacements = {
			"WAVE": {
				"replacement": self.wave(),
				"flags": re.MULTILINE | re.IGNORECASE
			},
			"USER(?:NAME|)": {
				"replacement": message.name,
				"flags": re.MULTILINE | re.IGNORECASE
			}
		}

		return self.subst_all(replacements=replacements, string=result)

def load():
	return Hello()