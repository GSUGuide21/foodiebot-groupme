from beta.arguments.base import Argument

class StringArgument(Argument):
	def run(self, **options):
		query = options.get("query", "")
		self.result = str(query)
		return self