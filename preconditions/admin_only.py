from beta.preconditions.base import Precondition

class AdminOnly(Precondition):
	def run(self, **options):
		group = options.get("group")
		user_id = options.get("message")["user_id"]
		user_ids = [user_id for user_id in group.admins.keys()]
		return user_id in user_ids