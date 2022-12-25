import os
import praw
from beta.commands.base import Command

class RedditCommand(Command):
	description = "Fetches information from the subreddit"
	argument_type = "spaces"

	def __init__(self):
		super(RedditCommand, self).__init__()

		self.provider = praw.Reddit(
			client_id=os.environ.get("praw_client_id"),
			client_secret=os.environ.get("praw_client_secret"),
			user_agent="foodiebotv2"
		)

	def parse_submission(self, submission):
		title = submission.title
		pass

	def respond(self, **options):
		args = options.get("args")
		sub_name = args.select("subreddit", "GaState")
		sort = args.select("sort", "top")
		limit = int(args.select("limit", "1"))

		subreddit = self.provider.subreddit(sub_name)
		
		match sort:
			case ["top", "t"]: submissions = subreddit.top(limit=limit)
			case ["hot", "h"]: submissions = subreddit.hot(limit=limit)
			case ["controversial", "c"]: submissions = subreddit.controversial(limit=limit)
			case ["new", "n"]: submissions = subreddit.new(limit=limit)
			case ["rising", "r"]: submissions = subreddit.rising(limit=limit)
			case _: submissions = subreddit.top(limit=limit)

		info = [self.parse_submission(submission) for submission in submissions]
		return str.join("\n", info)