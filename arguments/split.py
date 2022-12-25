from re import split, compile, MULTILINE
from beta.arguments.base import Argument

class SplitArgument(Argument):
	split_type = "string"
	delimiter = ""

	def __init__(self):
		self.result = []
	
	def validate(self, **options):
		command = options.get("command", None)
		if command is None: return False
		return len(self.result) >= command.min_arguments

	def split(self, string):
		if self.split_type == "pattern":
			return split(self.delimiter, string)

		return str.split(string, self.delimiter)

	def is_keyworded(self, string):
		pattern = compile(r'(?:"[^"]*"|\'[^\']*\')=(?:"[^"]*"|\'[^\']*\')', flags=MULTILINE)
		return pattern.match(string) is not None

	def run(self, **options):
		query = options.get("query", "")
		parts = self.split(query)
		
		args = []
		kwargs = {}

		for part in parts:
			if self.is_keyworded(part):
				pattern = compile(r'(?:"[^"]*"|\'[^\']*\')', flags=MULTILINE)
				key = part[0:part.index("=")]
				value = part[part.index("=")+1:]

				if pattern.match(key): 
					key = key[1:key.index("'" if key.startswith("'") else '"', 2)]
				if pattern.match(value):
					value = value[1:value.index("'" if value.startswith("'") else '"', 2)]
				
				kwargs[key] = value
			else:
				pattern = compile(r'(?:"[^"]*"|\'[^\']*\')', flags=MULTILINE)
				part = part[1:-1] if pattern.match(part) else part
				args.append(part)

		result = []

		for arg in args: result.append(arg)
		for key, value in kwargs.items():
			result.append(arg)

		self.result = result
		self.kwargs = kwargs

		return self

	def first(self):
		return self.result[0]

	def last(self):
		return self.result[-1]

	def select(self, key, default=None):
		return self.kwargs.get(key, default)

	def pickFirst(self):
		first = self.result.pop(0)
		return first

	def pickLast(self):
		last = self.result.pop()
		return last

	def pickFrom(self, key, default=None):
		if key in self.kwargs:
			value = self.kwargs.get(key)
			del self.kwargs[key]
			return value
		else:
			return default

	