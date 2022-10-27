import os
from .base import ImageCommand
from PIL import Image

cwd = os.getcwd()

class HereWeGo(ImageCommand):
	DESCRIPTION = 'Sends an "Ah shit, here we go again" meme'

	def has_args(self, query):
		return True

	def response(self, query, message, bot_id, app_id):
		image = Image.open("assets/images/herewego.gif")
		return "", self.upload_gif_image(image)