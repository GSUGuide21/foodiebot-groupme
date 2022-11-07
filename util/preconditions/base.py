class Precondition:
	PRECONDITION_WARNING = "You do not fit the requirements for this command. Try again later :("

	def __init__(self):
		print(f"Precondition ({self.__name__}) has been loaded!")
	
	def run(self, **options):
		pass