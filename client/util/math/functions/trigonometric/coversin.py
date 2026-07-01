from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def coversin(x: number) -> number:
	if isinstance(x, complex):
			return 1 - cmath.sin(x)
	return 1 - math.sin(x)
