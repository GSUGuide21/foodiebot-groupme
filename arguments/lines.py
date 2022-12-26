from arguments.split import SplitArgument

class LinesArgument(SplitArgument):
	delimiter = "\n"

def load(command=None):
	return LinesArgument(command)