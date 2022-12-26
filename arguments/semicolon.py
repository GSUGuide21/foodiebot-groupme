from re import compile, MULTILINE
from arguments.split import SplitArgument

class SemicolonArgument(SplitArgument):
	delimiter = compile(r'\s*(?:;)\s*(?=(?:[^"]|"[^"]*"|\'[^\']*\')*$)', MULTILINE)
	split_type = "pattern"

def load(command=None):
	return SemicolonArgument(command)