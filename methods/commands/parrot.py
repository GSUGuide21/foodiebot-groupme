import os, re
from .base import Command

class Parrot(Command):
	DESCRIPTION = "Parrots the user who prompted the command."
	CATEGORY = "Fun"
	ARGUMENT_TYPE = "string"
	ALIASES = ["copy"]

	def respond(self, **options):
		args = self.parse_arguments(options.get("query", ""))
		return args.result