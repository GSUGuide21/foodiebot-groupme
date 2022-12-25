import requests
from util import urljoin

class Manager:
	base_url = "https://api.groupme.com/v3/"

	def __init__(self, **options):
		self.path = options.get("path", None)
		self.url = urljoin(self.base_url, self.path)

	def __getitem__(self, key):
		return getattr(self, key)

	def __setitem__(self, key, value):
		return setattr(self, key, value)

	def get(self, **params):
		return requests.get(self.url, **params)
		
	def post(self, **params):
		return requests.post(self.url, **params)