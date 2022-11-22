from .base import Argument
from .string import StringArgument
from .integer import IntegerArgument
from .boolean import BooleanArgument
from .float import FloatArgument
from .group import GroupArgument
from .member import MemberArgument
from .lines import LinesArgument
from .split import SplitArgument
from .spaces import SpacesArgument
from .comma import CommaArgument
from .semicolon import SemicolonArgument
from .pipe import PipeArgument

arguments = {
	#Arguments
	"string": StringArgument,
	"float": FloatArgument,
	"comma": CommaArgument,
	"pipe": PipeArgument,
	"split": SplitArgument,
	"group": GroupArgument,
	"member": MemberArgument,
	"integer": IntegerArgument,
	"boolean": BooleanArgument,
	"spaces": SpacesArgument,
	"lines": LinesArgument,
	"semicolon": SemicolonArgument,
	#Aliases
	"str": "string",
	"int": "integer",
	"bool": "boolean",
}