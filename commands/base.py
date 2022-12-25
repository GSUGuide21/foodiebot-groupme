import os, sys
import random
import re
import requests

from preconditions import preconditions
from arguments import arguments
from manager import Group, ImageManager

from io import BytesIO
from PIL import ExifTags, Image, ImageSequence

class Command:
	aliases = []
	argument_type = "string"
	category = "Other"
	cooldown = 0
	description = "No description provided."
	min_arguments = 0
	preconditions = []
	warning = "Cannot activate command!"

	def __init__(self):
		self.access_token = os.environ.get("access_token")
		print(f"Command ({self.__class__.__name__}) has been loaded!")

	def __repr__(self):
		return f"Command ({self.__class__.__name__})"

	def wave(self):
		return "👋" + random.choice("🏻🏼🏽🏾🏿")

	def reply(self, **options):
		message = options.get("message")
		reply = options.get("reply", None)

		if reply == None or reply == "": return reply
		
		result = {}

		if isinstance(reply, (list, tuple)):
			text, image = reply
			result["text"] = text
			result["picture_url"] = image
		else:
			result = {"text": reply} if isinstance(reply, str) else reply

		params = {
			"type": "reply",
			"reply_id": message.id,
			"base_reply_id": message.id,
			"user_id": message.user_id
		}

		result["attachments"] = reply.get("attachments", [])

		for attachment in message.raw["attachments"]:
			if attachment["type"] == "reply":
				if attachment["type"]["base_reply_id"] != params["base_reply_id"]:
					params["base_reply_id"] = attachment["type"]["base_reply_id"]
					continue

		result.attachments.append(params)
		return result

	def mention(self, **options):
		users = options.get("users", [])
		reply = options.get("reply", None)

		if reply == None or reply == "": return reply
		if len(users) == 0: return reply

		result = {}

		if isinstance(reply, (list, tuple)):
			text, image = reply
			result["text"] = text
			result["picture_url"] = image
		else:
			result = {"text": reply} if isinstance(reply, str) else reply

		last_offset = 0
		mentions = []

		params = {
			"type": "mentions",
			"user_ids": [],
			"loci": []
		}

		for index, sender in enumerate(users):
			mention = f"@{sender.nick}"

			params["user_ids"].append(sender["user_id"])
			params["loci"].append([last_offset, len(mention)])

			mentions.append(mention)

			last_offset += len(mention) + 1

		mention_string = f"{str.join(' ', mentions)}"
		
		if result["text"] == None or result["text"] == "":
			result["text"] = mention_string
		else:
			result["text"] = f'{mention_string} {result["text"]}'

		result["attachments"] = reply.get("attachments", [])

		if len(result["attachments"]) > 0:
			for index, attachment in enumerate(result["attachments"]):
				if attachment["type"] == "mentions":
					if "user_ids" in attachment and isinstance(attachment["user_ids"], list):
						result["attachments"][index]["user_ids"] = attachment["user_ids"].extend(params["user_ids"])
						result["attachments"][index]["loci"] = attachment["loci"].extend(params["loci"])
						break

		else: result["attachments"].append(params)

		return result

	@property
	def args(self):
		t = self.argument_type.lower()
		t = t if t in arguments else "string"
		arg = arguments[t] if arguments in t else arguments["string"]
		
		if isinstance(arg, str): arg = arguments[arg] if arg in arguments else arguments["string"]
		return arg(self)

	def mention_owner(self, **options):
		group = options.get("group", None)
		reply = options.get("reply", None)
		if group is None: return reply
		return self.mention(reply=reply, users=[group.owner])

	def mention_admins(self, **options):
		group = options.get("group", None)
		reply = options.get("reply", None)
		if group is None: return reply
		admins = list(group.admins.values())
		return self.mention(reply=reply, users=admins)

	def mention_one(self, **options):
		user = options.get("user", None)
		reply = options.get("reply", None)
		return self.mention(reply=reply, users=[user])
		
	def mention_all(self, **options):
		at_everyone = self.client.state.get("everyone", False)
		reply = options.get("reply", None)
		if not at_everyone: return reply

		group = options.get("group", None)
		if group is None: return reply
		members = list(group.members.values())
		return self.mention(reply=reply, users=members)

	def run(self, **options):
		options["command"] = self
		all_preconditions = self.preconditions or []
		for precondition in all_preconditions:
			curr = preconditions[precondition]
			if not curr.validate(**options):
				return curr.warning
		return self.validate(**options)

	def validate(self, **options):
		if not self.is_valid(**options):
			return self.warning

		args = self.args.run(**options)
		result = args.result
		
		if isinstance(result, list) and len(result) < self.min_arguments:
			return self.warning

		options["args"] = args
		options["result"] = result
		return self.respond(**options)

	def is_valid(self, **options):
		return True

	def watch_for_cooldown(self):
		pass

	def respond(self, **options):
		pass

	@staticmethod
	def safe_spaces(text):
		text.replace("\t", " " * 4)
		return text.replace(" ", "\u2004")

	def normalize(self, text):
		return text.lower().replace(" ", "")

class ImageCommand(Command):
	def __init__(self, **options):
		super(ImageCommand, self).__init__(**options)
		self.image_manager = ImageManager()

	def upload_image(self, data, type="jpeg") -> str:
		headers = {
			"X-Access-Token": self.access_token,
			"Content-Type": f"image/{type}"
		}

		response = self.image_manager.post(data=data, headers=headers)
		return response.json()["payload"]["url"]

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