from __future__ import annotations

import os
import praw
from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, StringArgument, IntArgument


VALID_SORTS = ("hot", "new", "top", "rising", "controversial")

class RedditCommand(Command):
  name = "reddit"
  aliases = ["r"]
  description = "Fetch information from a subreddit"

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(
        StringArgument("subreddit", required=True),
        StringArgument("sort", required=False, default="top"),
        IntArgument("limit", required=False, default=1)
      )
    except ArgumentParseError:
      raise ValueError(f"Usage: {context.prefix}reddit <subreddit> [sort] [limit]")
    
    subreddit_name = parsed["subreddit"]
    sort = str(parsed["sort"] or "top").strip().lower()
    limit = parsed["limit"]

    if sort not in VALID_SORTS:
      raise ValueError(
        "Invalid sort option: "
        f"{sort}. Valid options are: {', '.join(VALID_SORTS)}."
      )

    if limit is None or limit < 1 or limit > 10:
      raise ValueError("limit must be between 1 and 10")

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
      return "reddit: missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET configuration."

    # Initialize the Reddit client
    reddit = praw.Reddit(
      client_id=client_id,
      client_secret=client_secret,
      user_agent="FoodieBot/1.0"
    )

    submissions = []

    # Fetch the subreddit
    try:
      subreddit = reddit.subreddit(subreddit_name)
      # Fetch the posts from the subreddit

      match sort.lower():
        case "hot":
          submissions = list(subreddit.hot(limit=limit))
        case "new":
          submissions = list(subreddit.new(limit=limit))
        case "top":
          submissions = list(subreddit.top(limit=limit))
        case "rising":
          submissions = list(subreddit.rising(limit=limit))
        case "controversial":
          submissions = list(subreddit.controversial(limit=limit))
        case _:
          raise ValueError(
            "Invalid sort option: "
            f"{sort}. Valid options are: {', '.join(VALID_SORTS)}."
          )
    except Exception as e:
      return f"Error fetching data from r/{subreddit_name}: {str(e)}"
    
    if not submissions:
      return f"No posts found in r/{subreddit_name} with sort '{sort}' and limit {limit}."
    
    # Format the response
    response = f"Top {limit} posts from r/{subreddit_name} sorted by '{sort}':\n"
    for submission in submissions:
      response += f"- {submission.title} (Score: {submission.score})\n  Link: {submission.url}\n"

    return response