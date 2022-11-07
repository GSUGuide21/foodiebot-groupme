import os, re, requests
from bs4 import BeautifulSoup, ResultSet, Tag
from selenium import webdriver
from urllib.parse import quote
from time import sleep
from .base import Command
from util import Argument
from ..driver import driver

CAMPUS_LABS_URL = "https://gsu.campuslabs.com/engage/events?perks=FreeFood"
CAMPUS_LABS_EVENT_PATH = "https://gsu.campuslabs.com/engage/event"

class Event(Command):
	DESCRIPTION = "Posts information about an event"
	MINIMUM_ARGUMENTS = 1
	ARGUMENT_TYPE = "spaces"
	CATEGORY = "Event"

	def respond(self, **options):
		args: Argument = self.parse_arguments(options.get("query", ""))
		
		return "Coming soom to a theater near you!"
		"""
		if args == None:
			return args.ARGUMENT_WARNING
		"""
		