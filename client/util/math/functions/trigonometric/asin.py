from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def asin(x: number) -> number:
	if isinstance(x, complex):
			return cmath.asin(x)
	return math.asin(x)
