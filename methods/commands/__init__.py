from .base import Command
from .coin import Coin
from .herewego import HereWeGo
from .random import Random
from .test import Test

commands = {
	"coin": Coin(),
	"herewego": HereWeGo(),
	"random": Random(),
	"test": Test()
}