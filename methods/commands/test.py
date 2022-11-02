import os, re, random, time, requests
from .base import Command

class Test(Command):
	DESCRIPTION = "Tests FoodieBot to check if it is working"
	LATENCY = 10
	ACCESS_TOKEN = os.environ.get("access_token")
	GROUP_ID = os.environ.get("group_id")
	API_ENDPOINT = "https://api.groupme.com/v3/groups"
	
	def response(self, query, message, bot_id, app_id):
		response = requests.get(f"{self.API_ENDPOINT}/{self.GROUP_ID}").json()["response"]
		print(response)
		time.sleep(self.LATENCY)
		return "Test completed!"