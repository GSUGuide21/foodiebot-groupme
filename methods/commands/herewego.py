from .base import ImageCommand
from PIL import Image

class HereWeGo(ImageCommand):
	DESCRIPTION = 'Sends an "Ah shit, here we go again" meme'

	def response(self):
		image = Image.open("assets/herewego.png")
		return "", self.upload_pil_image(image, "GIF")