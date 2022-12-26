from re import compile, MULTILINE
from arguments.split import SplitArgument

class SpacesArgument(SplitArgument):
	delimiter = compile(r'\s*(?=(?:[^"]|"[^"]*"|\'[^\']*\')*$)', MULTILINE)
	split_type = "pattern"

def load():
	return SpacesArgument()