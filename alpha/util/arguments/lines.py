from .split import SplitArgument

class LinesArgument(SplitArgument):
	def __init__(self, **options):
		super().__init__(delimiter="\n", **options)