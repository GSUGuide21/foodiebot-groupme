from preconditions.base import Precondition

class OwnerOnly(Precondition):
	def run(self, **options):
		group = options.get("group")
		user_id = options.get("message")["user_id"]
		return group.owner.user_id == user_id

def load():
	return OwnerOnly()