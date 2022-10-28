import os, re, random, time
from .base import Command

class Test(Command):
	DESCRIPTION = "Tests FoodieBot to check if it is working"
	
	def response(self, query, message, bot_id, app_id):
		latency = 3
		time.sleep(latency)
		return "Test completed in {latency}seconds".format(latency=latency)