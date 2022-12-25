from manager import *

class ImageManager(Manager):
	BASE_API_ENDPOINT = "https://image.groupme.com/pictures"

	def __init__(self, **options):
		super(ImageManager, self).__init__(**options)