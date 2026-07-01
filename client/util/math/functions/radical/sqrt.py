from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def sqrt(x: number) -> number:
  if isinstance(x, complex) or x < 0:
      return cmath.sqrt(x)
  return math.sqrt(x)