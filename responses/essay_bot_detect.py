import re
import random
from beta.responses.base import Response

class EssayBotDetect(Response):
	match_type = "pattern"
	pattern = re.compile(r"https?\://(?:(?:speedy?|e?x(?:tra|))-?essay(?:[sz]|service|)|paper(?:ok|c|z|s|g))\.(?:cf|ml|ga|gq)", flags=re.MULTILINE | re.IGNORECASE)

	def __init__(self):
		super(EssayBotDetect, self).__init__()
		with open("assets/responses/essaybot.txt") as f:
			self.responses = f.readlines()

	def respond(self, **options):
		message = options.get("message")
		group = options.get("group")
		if message is None: return None

		result = random.choice(self.responses)

		replacements = {
			"USER(?:NAME|)": {
				"replacement": message.name,
				"flags": re.MULTILINE | re.IGNORECASE
			},
			"GROUP": {
				"replaccement": group.name or "None",
				"flags": re.MULTILINE | re.IGNORECASE
			}
		}

		return self.subst_all(replacements=replacements, string=result)