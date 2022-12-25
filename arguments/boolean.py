import numpy
from arguments.base import Argument

class BooleanArgument(Argument):
	def run(self, **options):
		query = options.get("query", "")
		
		if numpy.isnan(query): result = query != ""
		else: result = bool(int(query))
		
		self.result = result
		return self

def load():
	return BooleanArgument()