from .base import Command
from .coin import Coin
from .event import Event
from .events import Events
from .herewego import HereWeGo
from .parrot import Parrot
from .random import Random
from .test import Test

commands = {
	"coin": Coin(),
	"event": Event(),
	"events": Events(),
	"herewego": HereWeGo(),
	"parrot": Parrot(),
	"random": Random(),
	"test": Test()
}