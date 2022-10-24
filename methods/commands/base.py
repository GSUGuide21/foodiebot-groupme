import os
import requests
import random
from io import BytesIO
from PIL import Image, ExifTags

API_URL = "https://api.groupme.com/v3/groups"
IMAGE_URL = "https://image.groupme.com/pictures"

class Command:
	DESCRIPTION = "No description."
	MINIMUM_ARGUMENTS = 0
	ARGUMENT_WARNING = "Not enough arguments provided! Please add more after the command."
	ACCESS_TOKEN = os.environ.get("access_token")

	def __init__(self):
		print(f"Command loaded {self.__class__.__name__}")
	
	def wave(self):
		return "👋" + random.choice("🏻🏼🏽🏾🏿")
	
	def handle_args(self, result):
		return result

	def lines(self, query):
		return [line for line in query.split("\n") if line != ""]

	def bullet(self, pairs, embellish_first=False) -> str:
		response = ""
		if embellish_first:
			if type(pairs) == tuple:
				pairs = list(pairs)
			title, value = pairs.pop(0)
			response += f"--- {title}: {value} --\n"
		for title, value in pairs:
			if value:
				response += f"{title}: {value}\n"
		return response
	
	@staticmethod
	def safe_spaces(text):
		text.replace("\t", " " * 4)
		return text.replace(" ", "\u2004")

	def normalize(self, text):
		return text.lower().replace(" ", "")

	def response(self, query, message, bot_id, app_id):
		pass

class ImageCommand(Command):
	def upload_image(self, data) -> str:
		headers = {
			"X-Access-Token": self.ACCESS_TOKEN,
			"Content-Type": "image/jpeg"
		}

		r = requests.post(IMAGE_URL, data=data, headers=headers)
		return r.json()["payload"]["url"]
	
	def rotate_upright(self, image: Image):
		try:
			for orientation in ExifTags.TAGS.keys():
				if ExifTags.TAGS[orientation] == "Orientation":
					break	
			
			exif = dict(image._getexif().items())

			orientation = exif[orientation]

			match orientation:
				case 3:
					image = image.rotate(180, expand=True)
				case 6:
					image = image.rotate(270, expand=True)
				case 8:
					image = image.rotate(90, expand=True)

		except (AttributeError, KeyError) as e:
			pass

		return image

	def upload_pil_image(self, image: Image):
		output = BytesIO()
		image.save(output, format="JPEG", mode="RGB")
		return self.upload_image(output.getvalue())

	def pil_from_url(self, url):
		response = requests.get(url, stream=True)
		response.raw.decode_content = True
		image = Image.open(response.raw)

		image = self.rotate_upright(image)
		image = image.convert("RGB")

		return image

	def resize(self, image: Image, width):
		natural_width, natural_height = image.size
		height = int(width * natural_height / natural_width)
		image = image.resize((width, height), Image.ANTIALIAS)
		return image

	def limit_image_size(self, image: Image, max_width=1000):
		natural_width, natural_height = image.size
		if natural_width > max_width:
			image = self.resize(image, max_width)
		return image

	def get_portrait(self, user_id, group_id):
		members = requests.get(f"{API_URL}/${group_id}?token=${self.ACCESS_TOKEN}").json()["response"]["members"]
		for member in members:
			if member["user_id"] == user_id:
				return member["image_url"]

	def get_source_url(self, message, include_avatar=True):
		mention_attachments = [attachment for attachment in message.raw["attachments"] if attachment["type"] == "mentions"]
		if message.image_url is not None:
			return message.image_url
		elif len(mention_attachments) > 0:
			return self.get_portrait(mention_attachments[0]["user_ids"][0], message.group_id)
		
		if include_avatar:
			return message.avatar_url