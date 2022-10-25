from .base import Command
from .coin import Coin
from .herewego import HereWeGo

commands = {
	"coin": Coin(),
	"herewego": HereWeGo()
}