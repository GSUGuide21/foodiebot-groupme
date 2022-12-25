from manager.group import Member
from arguments.base import Argument

class MemberArgument(Argument):
	warning = "Invalid member ID or key!"
	def validate(self, **options):
		return options.get("query", "") != ""

	def run(self, **options):
		query = options.get("query", "")
		member_id = query
		self.result = Member(id=member_id)
		return self

def load():
	return MemberArgument()