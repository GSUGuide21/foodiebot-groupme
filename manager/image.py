from .base import Manager

class ImageManager(Manager):
	BASE_API_ENDPOINT = "https://image.groupme.com/"

	def __init__(self, **options):
		super(ImageManager, self).__init__(**options)