import os, re
from .base import Command

class Parrot(Command):
	DESCRIPTION = "Parrots the user who prompted the command."

	def has_args(self, query):
		return query != None or query != ""

	def response(self, query, message, bot_id, app_id):
		return query