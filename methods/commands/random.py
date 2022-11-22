import os
import re
from random import randint
from .base import Command

class Random(Command):
	DESCRIPTION = "Rolls a die on a random number"
	ALIASES = ["roll", "dice"]
	ARGUMENT_TYPE = "spaces"
	CATEGORY = "Fun"
	
	def handle_bounds(self, result: list[str] | None):
		a, b = result

		a = a if a != None or a != "" else 0
		b = b if b != None or b != "" else 5

		a = int(a)
		b = int(b)

		_min = min(a, b)
		_max = max(a, b)

		return {
			"min": _min,
			"max": _max
		}

	def ok(self, **options):
		query = options.get('query', '')
		args = self.parse_arguments(query=query)
		bounds = self.handle_bounds(args.result)
		result = randint(bounds["min"], bounds["max"])

		return f"FoodieBot has rolled a die! The number landed on {result}"
