from manager import Manager

class BotManager(Manager):
	def __init__(self):
		super(BotManager, self).__init__(path="bots")