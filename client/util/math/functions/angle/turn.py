from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import math

def turn(x: number, type: str = "radians") -> number:
	if isinstance(x, complex):
		return complex(turn(x.real, type), turn(x.imag, type))

	match type:
		case "radians":
			return x / (2 * math.pi)
		case "degrees":
			return x / 360
		case "grad" | "gradians":
			return x / 400
		case "turn" | "turns":
			return x
		case _:
			raise DomainError(f"Invalid type '{type}' for turn function. Valid types are 'radians', 'degrees', 'grad', 'gradians', 'turn', or 'turns'.")
