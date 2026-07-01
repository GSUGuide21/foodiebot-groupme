from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def atan2(x: number, y: number) -> number:
  if isinstance(x, complex) or isinstance(y, complex):
    return cmath.tan(y / x)
  return math.atan2(x, y)