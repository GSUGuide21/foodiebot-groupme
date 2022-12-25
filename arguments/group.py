from beta.manager.group import Group
from beta.arguments.base import Argument

class GroupArgument(Argument):
	warning = "Invalid group ID or key!"
	def validate(self, **options):
		return options.get("query", "") != ""

	def run(self, **options):
		query = options.get("query", "")

		if query == "current":
			group_id = options.get("group").id
		else:
			group_id = query

		self.result = Group(id=group_id)
		return self

def load():
	return GroupArgument()