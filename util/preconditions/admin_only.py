from .base import Precondition
from ..group import Group

class AdminOnly(Precondition):
	def run(self, **options):
		group: Group = options["group"]
		user_id = options["message"]["user_id"]
		admins = [admin_user_id for admin_user_id in group.admins.keys()]
		return user_id in admins