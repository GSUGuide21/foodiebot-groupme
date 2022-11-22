from .base import Argument

class FloatArgument(Argument):
	def __init__(self):
		pass

	def ok(self, **options):
		query = options.get('query', "")
		return float(query)