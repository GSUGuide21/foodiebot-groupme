import os
from .base import ImageCommand
from PIL import Image

cwd = os.getcwd()

class HereWeGo(ImageCommand):
	DESCRIPTION = 'Sends an "Ah shit, here we go again" meme'
	CATEGORY = "Image"

	def respond(self, **options):
		image = Image.open("assets/images/herewego.gif")
		return "", self.upload_gif_image(image)