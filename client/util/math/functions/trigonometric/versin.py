from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def versin(x: number) -> number:
	if isinstance(x, complex):
			return 1 - cmath.cos(x)
	return 1 - math.cos(x)
