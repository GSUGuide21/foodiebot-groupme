import requests
from util import urljoin

class Manager:
	BASE_API_ENDPOINT = "https://api.groupme.com/v3/"

	def __init__(self, **options):
		self.path = options.get("path", None)
		self.url = urljoin(self.BASE_API_ENDPOINT, self.path)

	def __getitem__(self, key):
		return getattr(self, key)

	def __setitem__(self, key, value):
		return setattr(self, key, value)