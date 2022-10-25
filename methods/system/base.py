import re
import random
from ..commands import Command

class SystemCommand(Command):
	def get_names(self, query: str) -> str:
		results = self.REGEX.findall(query).pop()
		results = [result for result in results if result not in ("", "re")]
		return results.pop().replace(" and ", ", ").split(", ")