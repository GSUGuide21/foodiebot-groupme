from .split import SplitArgument
from methods.commands import Command

class LinesArgument(SplitArgument):
	def __init__(self, **options):
		super().__init__(delimiter="\n", **options)