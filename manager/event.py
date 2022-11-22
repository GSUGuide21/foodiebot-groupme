from .base import Manager

class EventManager(Manager):
	BASE_API_ENDPOINT = "https://gsu.campuslabs.com/engage/events"

	def __init__(self, **options):
		super(EventManager, self).__init__(**options)
		