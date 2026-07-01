from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def asech(x: number) -> number:
  if isinstance(x, complex):
      return cmath.acosh(1 / x)
  return math.acosh(1 / x)