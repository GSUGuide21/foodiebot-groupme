from numpy import isnan
from beta.arguments.base import Argument

class FloatArgument(Argument):
	def run(self, **options):
		query = options.get("query", "")
		if isnan(query): result = "NaN"
		else: result = float(query)
		
		self.result = result
		return self

def load():
	return FloatArgument()