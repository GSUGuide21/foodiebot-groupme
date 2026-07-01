from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def tan(x: number) -> number:
  if isinstance(x, complex):
      return cmath.tan(x)
  return math.tan(x)