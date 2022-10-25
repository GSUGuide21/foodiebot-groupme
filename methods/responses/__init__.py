from .hello import Hello
from .essay_bot_detect import EssayBotDetect

responses = {
	"essaybot": EssayBotDetect(),
	"hello": Hello()
}