import random
from .base import Command

class Coin(Command):
	DESCRIPTION = "Flips a coin!"
	ALIASES = ["flip", "coinflip"]
	COINS = ["heads", "tails"]

	def has_args(self, query):
		return len(self.spaces(query)) >= self.MINIMUM_ARGUMENTS

	def handle_args(self, query: str | None=""):
		if query is None or query == "":
			return query
		
		parts = self.spaces(query)
		display = parts[0]

		return display.lower()
	
	def response(self, query, message, bot_id, app_id):
		display = self.handle_args(query)
		result = random.choice(self.COINS)

		if display is not "" or display is not None:
			match display:
				case "upper":
					result = result.upper()
				case "lower":
					result = result.lower()
				case "fl":
					result = result[0].upper()
				case "flupper":
					result = result[0].upper()
				case "fllower":
					result = result[0].lower()
	
		return f"FoodieBot has flipped a coin! It landed on {result}"