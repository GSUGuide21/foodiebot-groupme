from commands.base import Command

class Parrot(Command):
	description = "Parrots the user who prompted the command."
	category = "Fun"
	argument_type = "string"
	aliases = ["copy"]
	warning = "Whoa cowboy! I need some words, man!"

	def is_valid(self, **options):
		return options.get("query", "") != ""

	def respond(self, **options):
		result = options.get("result")
		message = options.get("message")
		reply = {"text": result}

		return self.reply(reply=reply, message=message)

def load():
	return Parrot()