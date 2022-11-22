from ..util import urljoin

class Manager:
	BASE_API_ENDPOINT = "https://api.groupme.com/v3/"

	def __init__(self, **options):
		self.path = options.get("path", None)
		self.url = urljoin(self.BASE_API_ENDPOINT, self.path)