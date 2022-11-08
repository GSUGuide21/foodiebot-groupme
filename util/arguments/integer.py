from .base import Argument

class IntegerArgument(Argument):
	def __init__(self):
		pass

	def ok(self, **options):
		query = options.get('query', "")
		return int(query)