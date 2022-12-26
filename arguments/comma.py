from re import compile, MULTILINE
from arguments.split import SplitArgument

class CommaArgument(SplitArgument):
	delimiter = compile(r'\s*(?:,)\s*(?=(?:[^"]|"[^"]*"|\'[^\']*\')*$)')
	split_type = "pattern"

def load(command=None):
	return CommaArgument(command)