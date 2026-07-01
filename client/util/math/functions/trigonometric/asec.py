from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def asec(x: number) -> number:
	if isinstance(x, complex):
			return cmath.acos(1 / x)
	return math.acos(1 / x)
