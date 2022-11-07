from re import compile, MULTILINE
from .split import SplitArgument

class PipeArgument(SplitArgument):
	def __init__(self, **options):
		delimiter = compile(r"\|", flags=MULTILINE)
		super().__init__(delimiter=delimiter, split_type="pattern", **options)