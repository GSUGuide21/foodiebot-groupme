from enum import Enum

class SenderType(Enum):
	Bot = "bot"
	User = "user"
	System = "system"
	Service = "service"