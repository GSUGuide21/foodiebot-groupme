import os
import random
import re
from .base import Command

class Random(Command):
	DESCRIPTION = "Rolls a die on a random number"
	ALIASES = ["roll", "dice"]
	ARGUMENT_TYPE = "spaces"
	CATEGORY = "Fun"
	
	def handle_bounds(self, result: list[str] | None):
		a = int(result[0] or 0)
		b = int(result[1] or 5)

		_min = min(a, b)
		_max = max(a, b)

		return {
			"min": _min,
			"max": _max
		}

	def respond(self, **options):
		args = self.parse_arguments(options.get("query", ""))
		bounds = self.handle_bounds(args.result)
		result = random.randint(bounds["min"], bounds["max"])

		return f"FoodieBot has rolled a die! The number landed on {result}"