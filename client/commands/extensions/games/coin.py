from __future__ import annotations

import random

from client.commands.base import Command


class CoinCommand(Command):
  name = "coin"
  aliases = ["flip", "c"]
  description = "Flip a coin"
  timeout_seconds = 2

  def execute(self, message, context):
    coins = ["Heads", "Tails"]
    result = random.choice(coins)
    return f"FoodieBot flipped a coin and it landed on {result}!"
