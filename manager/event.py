from manager import *

class Event:
	def __init__(self, **options):
		self.raw = options

		self.name = options.get("name")
		self.description = options.get("description", "No description provided.")
		self.location = options.get("location", {})
		self.start = options.get("start_at")
		self.end = options.get("end_at")
		self.is_all_day = options.get("is_all_day", False)
		self.timezone = options.get("timezone")
		self.reminders = options.get("reminders", [])
		self.id = options.get("event_id")
		self.created = options.get("created_at")
		self.updated = options.get("updated_at")
		self.deleted = options.get("deleted_at", None)

		self.creator = Member(id=options.get("creator_id"))

	def __eq__(self, other):
		return self.id == other.id

	@property
	def going(self):
		members = [Member(id=id) for id in self.raw["going"]]
		return members

	@property
	def not_going(self):
		members = [Member(id=id) for id in self.raw["not_going"]]
		return members