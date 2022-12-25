from beta.commands.base import ImageCommand
from PIL import Image

class HereWeGo(ImageCommand):
	description = 'Sends an "Ah shit, here we go again" meme'
	category = "Image"

	def respond(self, **options):
		result = options.get("result", "")
		image = Image.open("assets/image/herewego.gif")
		return result, self.upload_gif_image(image)

def load(client):
	return HereWeGo(client)