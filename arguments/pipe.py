from re import compile, MULTILINE
from arguments.split import SplitArgument

class PipeArgument(SplitArgument):
	delimiter = compile(r'\s*(?:\|)\s*(?=(?:[^"]|"[^"]*"|\'[^\']*\')*$)', MULTILINE)
	split_type = "pattern"

def load(command=None):
	return PipeArgument(command)