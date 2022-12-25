from numpy import isnan
from beta.arguments.base import Argument

class IntegerArgument(Argument):
	def run(self, **options):
		query = options.get("query", "")
		if isnan(query): result = "NaN"
		else: result = int(query)
		
		self.result = result
		return self

def load():
	return IntegerArgument()