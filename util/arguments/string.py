from .base import Argument

class StringArgument(Argument):
	def __init__(self):
		super().__init__()

	def __repr__(self):
		return self.result

	def ok(self, **options):
		query = options.get("query", "")
		self.result = str(query)
		return self