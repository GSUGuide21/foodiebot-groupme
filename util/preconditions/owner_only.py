from ..group import Group
from .base import Precondition

class OwnerOnly(Precondition):
	def __init__(self):
		pass

	def run(self, **options):
		group: Group = options["group"]
		user_id = options["message"]["user_id"]
		owner = group.owner
		return owner.user_id == user_id