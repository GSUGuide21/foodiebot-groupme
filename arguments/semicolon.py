from re import compile, MULTILINE
from beta.arguments.split import SplitArgument

class SemicolonArgument(SplitArgument):
	delimiter = compile(r'\s*(?:;)\s*(?=(?:[^"]|"[^"]*"|\'[^\']*\')*$)', MULTILINE)
	split_type = "pattern"

def load():
	return SemicolonArgument()