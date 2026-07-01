from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def acsc(x: number) -> number:
	if isinstance(x, complex):
			return cmath.asin(1 / x)
	return math.asin(1 / x)
