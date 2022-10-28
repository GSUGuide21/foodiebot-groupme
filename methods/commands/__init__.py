from .base import Command
from .coin import Coin
from .herewego import HereWeGo
from .random import Random
from .events import Events
from .test import Test

commands = {
	"coin": Coin(),
	"herewego": HereWeGo(),
	"random": Random(),
	"events": Events(),
	"test": Test()
}