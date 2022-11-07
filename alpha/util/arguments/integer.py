from .base import Argument

class IntegerArgument(Argument):
	def __init__(self):
		pass

	def run(self, **options):
		query = options.get('query', "")