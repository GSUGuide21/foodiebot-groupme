class Precondition:
	warning = "You do not fit the requirements for this command. Try again later :("

	def __init__(self):
		print(f"Precondition ({self.__class__.__name__}) has been loaded!")

	def __repr__(self):
		return f"Precondition ({self.__class__.__name__})"

	def run(self, **options):
		pass