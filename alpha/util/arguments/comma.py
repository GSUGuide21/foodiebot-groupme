from re import compile, MULTILINE
from .split import SplitArgument

class CommaArgument(SplitArgument):
	def __init__(self, **options):
		delimiter = compile(r"\s*,\s*", flags=MULTILINE)
		super().__init__(delimiter=delimiter, split_type="pattern", **options)