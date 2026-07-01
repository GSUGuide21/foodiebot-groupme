from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def cos(x: number) -> number:
  if isinstance(x, complex):
      return cmath.cos(x)
  return math.cos(x)