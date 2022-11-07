from enum import Enum

class SenderType(Enum):
	User = "user"
	Bot = "bot"
	System = "system"
	Service = "service"