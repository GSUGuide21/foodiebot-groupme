from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def log2(x: number) -> number:
  if isinstance(x, complex):
      return cmath.log(x, 2)
  return math.log2(x)