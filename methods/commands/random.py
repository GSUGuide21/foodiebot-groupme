import os
import random
import re
from .base import Command

class Random(Command):
	def handle_args(self, result: str | None):
		result = [result for result in self.spaces(result)]

		a = int(result[0] or 0)
		b = int(result[1] or 5)

		_min = min(a, b)
		_max = max(a, b)

		return {
			"min": _min,
			"max": _max
		}

	def response(self, query, message, bot_id, app_id):
		bounds = self.handle_args(query)
		result = random.randint(bounds["min"], bounds["max"])

		return f"FoodieBot has rolled a die! The number landed on {result}"