import re
from .base import Argument

class SplitArgument(Argument):
	def __init__(self, **options):
		self.split_type = options.get("split_type", "string")
		self.delimiter = options["delimiter"]
		self.limit = options.get("limit", float('inf'))
		self.result = []

	def validate(self, **options):
		command = options["command"]
		return len(self.result) >= command.MINIMUM_ARGUMENTS

	def split(self, string):
		match self.split_type:
			case "string":
				return str.split(string, self.delimiter)
			case "pattern":
				return re.split(self.delimiter, string)

		return str.split(string, self.delimiter)

	def ok(self, **options):
		if not self.validate(**options):
			return self.ARGUMENT_WARNING
			
		query: str = options.get("query", "")
		parts = str.split(query, self.delimiter)
		self.result = parts
		return self