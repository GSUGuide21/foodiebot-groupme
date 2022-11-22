import os, re
from .base import Command

class Parrot(Command):
	DESCRIPTION = "Parrots the user who prompted the command."
	CATEGORY = "Fun"
	ARGUMENT_TYPE = "string"
	ALIASES = ["copy"]
	ARGUMENT_WARNING = "Whoa cowboy! I need some words, man!"

	def is_valid(self, **options):
		return options.get("query", "") != ""

	def error(self, **options):
		return self.ARGUMENT_WARNING

	def ok(self, **options):
		args = self.parse_arguments(options.get("query", ""))
		return args.result