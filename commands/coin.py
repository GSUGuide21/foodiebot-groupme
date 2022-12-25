from beta.commands.base import Command
from random import choice

class Coin(Command):
	description = "Performs a coin flip"
	aliases = ["flip", "coinflip"]
	coins = ["heads", "tails"]
	category = "Fun"
	argument_type = "spaces"

	displays = {
		"up": lambda r: r.upper(),
		"lo": lambda r: r.lower(),
		"fl": lambda r: r[0]
	}

	def respond(self, **options):
		result = options.get("result", [])
		result = [r.lower() for r in result]
		coin = choice(self.coins)

		if len(result) > 0:
			flags = [f for f in result if f in ["up", "lo"]]

			if flags[0] == "up": result.remove("lo")
			elif flags[0] == "lo": result.remove("up")

			for flag in result: coin = self.displays[flag](coin)

		return f"FoodieBot has flipped a coin! It landed on {coin}"

def load(client):
	return Coin(client)