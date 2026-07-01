from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def acoth(x: number) -> number:
  if isinstance(x, complex):
      return cmath.atanh(1 / x)
  return math.atanh(1 / x)