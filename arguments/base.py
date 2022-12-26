class Argument:
	warning = "You do not have enough arguments for me to run this command!"

	def __init__(self):
		self.result = None
		print(f"Argument ({self.__class__.__name__}) has been loaded!")

	def __repr__(self):
		return f"Argument ({self.__class__.__name__})"

	def validate(self, **options):
		return True

	def run(self, **options):
		return self