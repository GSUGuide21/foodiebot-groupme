import os
import random
import re
from typing import TypeVar
from io import BytesIO

import requests
from PIL import ExifTags, Image, ImageSequence

from manager import Group, ImageManager, Manager
from util import Argument, arguments, preconditions

T = TypeVar("T")

class Command(ImageManager):
	DESCRIPTION = "No description provided!"
	MINIMUM_ARGUMENTS = 0
	PRECONDITIONS = []
	ALIASES = []
	CATEGORY = "None"
	ARGUMENT_TYPE = "string"

	def __init__(self):
		super().__init__(path="pictures")
		self.access_token = os.environ.get("access_token")
		print(f"Command ({self.__class__.__name__}) has been loaded!")

	def wave(self):
		return "👋" + random.choice("🏻🏼🏽🏾🏿")

	def mention_users(self, **options):
		reply = options.get("reply", None)
		user_ids = options.get("user_ids", [])

		if len(user_ids) == 0: return reply
		if reply == None or reply == "": return reply

		result = {}

		if isinstance(reply, str):
			result["text"] = reply
		elif isinstance(reply, (tuple, list)):
			text, image = reply
			result["text"] = text
			result["picture_url"] = image
		else:
			result = reply

		if result.get("picture_url") or result["text"]:
			result["attachments"] = result["attachments"] or []
			if len(result["attachments"]) > 0:
				for index, attachment in enumerate(result["attachments"]):
					if attachment["type"] == "mentions":
						if "user_ids" in attachment and isinstance(attachment["user_ids"], list):
							result["attachments"][index]["user_ids"] = attachment["user_ids"].extend(user_ids)
							break
			else:
				result["attachments"].append({
					"type": "mentions",
					"user_ids": user_ids
				})

		return result


	def mention(self, **options):
		reply = options.get("reply", None)
		sender = options.get("sender", None)

		if sender is None: return reply
		if reply == None or reply == "": return reply

		result = {}

		if isinstance(reply, str):
			result["text"] = reply
		elif isinstance(reply, (tuple, list)):
			text, image = reply
			result["text"] = text
			result["picture_url"] = image
		else:
			result = reply

		if result.get("picture_url") or result["text"]:
			user_id = sender["user_id"]
			result["attachments"] = result.get("attachments", [])
			if len(result["attachments"]) > 0:
				for index, attachment in enumerate(result["attachments"]):
					if attachment["type"] == "mentions":
						if "user_ids" in attachment and isinstance(attachment["user_ids"], list):
							result["attachments"][index]["user_ids"] = attachment["user_ids"].extend(user_id)
							break
			else:
				result["attachments"].append({
					"type": "mentions",
					"user_ids": [user_id]
				})

		return result

	def bullet(self, **options) -> str:
		pairs = options.get("pairs")
		embellish_first = options.get("embellish_first", False)

		response = ""
		if embellish_first:
			if type(pairs) == tuple:
				pairs = list(pairs)
			title, value = pairs.pop(0)
			response += f"--- {title}: {value} ---\n"

		for title, value in pairs:
			if value: response += f"{title}: {value}\n"
		
		return response.strip()

	def validate(self, **options):
		for key, precondition in preconditions.items():
			if key in self.PRECONDITIONS:
				if precondition.run(**options):
					return True

		return self.is_valid(**options)

	def is_valid(self, **options):
		return True

	@property
	def args(self) -> Argument:
		arg_type = self.ARGUMENT_TYPE.lower()
		arg_type = arg_type if arg_type in arguments else "string"
		target = arguments[arg_type]

		if isinstance(target, str):
			if target in arguments:
				target = arguments[target]
			else:
				target = arguments["string"]

		return target()

	def parse_arguments(self, **options):
		return self.args.run(**options)

	@staticmethod
	def safe_spaces(text):
		text.replace("\t", " " * 4)
		return text.replace(" ", "\u2004")

	def normalize(self, text):
		return text.lower().replace(" ", "")

	def ok(self, **options):
		pass

	def error(self, **options):
		pass

	def respond(self, **options):
		return self.ok(**options) if self.validate(**options) else self.error(**options)

class ImageCommand(Command):
	def upload_image(self, data, type="jpeg") -> str:
		headers = {
			"X-Access-Token": self.access_token,
			"Content-Type": f"image/{type}"
		}

		r = requests.post(self.url, data=data, headers=headers)
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

	def upload_pil_image(self, image: Image, image_format="JPEG"):
		output = BytesIO()
		image.save(output, format=image_format, mode="RGB")
		return self.upload_image(output.getvalue())

	def upload_gif_image(self, original: Image):
		output = BytesIO()
		duration = original.info["duration"]
		frames = iter([frame.copy() for frame in ImageSequence.Iterator(original)])
		image = next(frames)
		image.save(output, format="GIF", append_images=frames, duration=duration/2000.0, loop=1, mode="RGB")
		return self.upload_image(output.getvalue(), "gif")

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

	def get_portrait(self, user_id, group: Group):
		member = group.fetch().find_member(user_id)
		if member["image_url"]:
			return member["avatar_url"]

	def get_source_url(self, message, include_avatar=True):
		mention_attachments = [attachment for attachment in message.raw["attachments"] if attachment["type"] == "mentions"]
		if message.image_url is not None:
			return message.image_url
		elif len(mention_attachments) > 0:
			return self.get_portrait(mention_attachments[0]["user_ids"][0], message.group_id)
		
		if include_avatar:
			return message.avatar_url