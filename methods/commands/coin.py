from random import choice
from .base import Command

class Coin(Command):
	DESCRIPTION = "Performs a coin flip!"
	ALIASES = ["flip", "coinflip"]
	COINS = ["heads", "tails"]
	ARGUMENT_TYPE = "string"
	CATEGORY = "Event"

	DISPLAYS = {
		"upper": lambda r: r.upper(),
		"lower": lambda r: r.lower(),
		"fl": lambda r: r[0],
		"flupper": lambda r: r[0].upper(),
		"fllower": lambda r: r[0].lower()
	}

	def ok(self, **options):
		query = options.get("query", "")
		coin = choice(self.COINS)
		display = self.parse_arguments(query=query)

		print(display, query)

		result = ""
		if display.result in self.DISPLAYS:
			curr = self.DISPLAYS[display]
			result = curr(coin)
		else: result = coin

		return f"FoodieBot has flipped a coin! It landed on {result}"