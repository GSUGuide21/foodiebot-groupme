import os
import re
import random

from beta.preconditions import preconditions

class Response:
	preconditions = []
	cooldown = 0
	match_type = "string"
	pattern = None
	triggers = []

	def __init__(self):
		self.access_token = os.environ.get("access_token")
		print(f"Response ({self.__class__.__name__}) has been loaded!")

	def __repr__(self):
		return f"Response ({self.__class__.__name__})"

	def wave(self):
		return "👋" + random.choice("🏻🏼🏽🏾🏿")
	
	def subst(self, **options):
		pattern = self.create_pattern(**options)
		string = options.get("string", "")
		replacement = options.get("replacement", "")
		count = options.get("count", 0)

		if pattern == None: return string
		return pattern.sub(replacement, string, count)

	def subst_all(self, **options):
		replacements = options.get("replacements", {})
		string = options.get("string", "")
		
		for key, sub in replacements.items():
			sub["pattern"] = key
			string = self.subst(**sub)

		return string

	def create_pattern(self, **options):
		flags = options.get("flags", None)
		pattern = options.get("pattern", None)

		if pattern == None: return None

		if flags != None: return re.compile(fr"%{pattern}%", flags=flags)
		else: return re.compile(fr"%{pattern}%")

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

	def validate(self, **options):
		options["response"] = self
		all_preconditions = self.preconditions or []
		for precondition in all_preconditions:
			curr = preconditions[precondition]
			if not curr.validate(**options):
				return False
		return self.is_valid(**options)

	def is_valid(self, **options):
		query = options.get("message").text
		if self.match_type == "pattern":
			return re.match(self.pattern, query) is not None
		else:
			triggers = [trigger.lower() for trigger in self.triggers if trigger != ""]
			return query.lower() in triggers

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