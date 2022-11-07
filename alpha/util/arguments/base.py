class Argument:
	ARGUMENT_WARNING = "You do not have enough arguments for me to run this command. I NEEEED MOOOOORE!!"

	def __init__(self, **options):
		self.message = options["message"]
		self.command = options["command"]
		self.group = options["group"]
		self.query = options["query"]

		self.initial_value = self.query
		self.value = self.query

	def validate(self):
		return True

	def run(self, **options):
		return self