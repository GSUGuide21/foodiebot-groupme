from arguments.split import SplitArgument

class LinesArgument(SplitArgument):
	delimiter = "\n"

def load():
	return LinesArgument()