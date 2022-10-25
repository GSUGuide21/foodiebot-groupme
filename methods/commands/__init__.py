from .base import Command
from .coin import Coin
from .herewego import HereWeGo
from .random import Random

commands = {
	"coin": Coin(),
	"herewego": HereWeGo(),
	"random": Random()
}