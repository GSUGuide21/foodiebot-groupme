from beta.commands.base import Command
from random import randint

class Roll(Command):
	description = "Rolls a die on a random number"
	aliases = ["dice", "random"]
	argument_type = "spaces"
	category = "Fun"

	def get_bounds(self, result):
		a, b = tuple(result)

		a = int(a if a != None or a != "" else 0)
		b = int(b if b != None or b != "" else 5)

		_min, _max = (min(a, b), max(a, b))

		r = {"min": _min, "max": _max}
		return r

	def respond(self, **options):
		result = options.get("result", "")
		bounds = self.get_bounds(result)
		r = randint(bounds["min"], bounds["max"])

		return f"FoodieBot has rolled a die! The number landed on {r}"