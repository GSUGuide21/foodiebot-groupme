from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def acsch(x: number) -> number:
  if isinstance(x, complex):
      return cmath.asinh(1 / x)
  return math.asinh(1 / x)