import os, re, requests
from time import sleep
from .member import Member

class Group:
	# Constants
	API_ENDPOINT = "https://api.groupme.com/v3/groups"
	ACCESS_TOKEN = os.environ.get("access_token")
	# Variables
	members = {}

	def __init__(self, group_id):
		response = requests.get(f"{self.API_ENDPOINT}/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]

		self.group_id = group_id
		self.message_count = response["messages"]["count"]

		self.generate_users(response["members"])
		

	def generate_users(self, members):
		for member in members:
			self.members[member["user_id"]] = Member(member)