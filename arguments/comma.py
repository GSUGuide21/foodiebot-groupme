from re import compile, MULTILINE
from beta.arguments.split import SplitArgument

class CommaArgument(SplitArgument):
	delimiter = compile(r'\s*(?:,)\s*(?=(?:[^"]|"[^"]*"|\'[^\']*\')*$)')
	split_type = "pattern"

def load():
	return CommaArgument()