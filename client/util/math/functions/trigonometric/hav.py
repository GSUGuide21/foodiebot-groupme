from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def hav(x: number) -> number:
	if isinstance(x, complex):
			return (1 - cmath.cos(x)) / 2
	return (1 - math.cos(x)) / 2
