class Argument:
	ARGUMENT_WARNING = "You do not have enough arguments for me to run this command. I NEEEED MOOOOORE!!"

	def __init__(self):
		print(f"Argument ({self.__class__.__name__}) has been loaded!")

	def validate(self, **options):
		return True

	def run(self, **options):
		return self