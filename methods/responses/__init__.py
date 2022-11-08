from .base import Response
from .essay_bot_detect import EssayBotDetect
from .hello import Hello
from .say import Say


responses = {
	"essay_bot_detect": EssayBotDetect(),
	"hello": Hello(),
	"say": Say()
}