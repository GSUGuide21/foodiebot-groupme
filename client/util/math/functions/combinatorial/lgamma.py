from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError
from client.util.math.functions.combinatorial.gamma import gamma

import cmath
import math

def lgamma(x: number) -> number:
	if isinstance(x, complex):
		if x.imag == 0 and x.real <= 0 and float(x.real).is_integer():
			raise DomainError("Gamma is undefined for non-positive integers.")
		return cmath.log(gamma(x))
	return math.lgamma(x)
