from random import choice
from .base import Command

class Coin(Command):
	DESCRIPTION = "Flips a coin!"
	ALIASES = ["flip", "coinflip"]
	COINS = ["heads", "tails"]
	
	ARGUMENT_TYPE = "string"
	CATEGORY = "Event"

	def respond(self, **options):
		query = options.get("query", "")
		display = self.parse_arguments(query)
		coin = choice(self.coins)

		displays = {
			"upper": lambda r: r.upper(),
			"lower": lambda r: r.lower(),
			"fl": lambda r: r[0],
			"flupper": lambda r: r[0].upper(),
			"fllower": lambda r: r[0].lower()
		}

		result = displays[display](coin) if display in displays else coin

		return f"FoodieBot has flipped a coin! It landed on {result}"