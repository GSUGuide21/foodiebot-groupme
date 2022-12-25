from re import compile, MULTILINE
from beta.arguments.split import SplitArgument

class PipeArgument(SplitArgument):
	delimiter = compile(r'\s*(?:\|)\s*(?=(?:[^"]|"[^"]*"|\'[^\']*\')*$)', MULTILINE)
	split_type = "pattern"

def load():
	return PipeArgument()