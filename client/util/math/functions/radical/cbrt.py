from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath

def cbrt(x: number) -> number:
  if isinstance(x, complex):
      return cmath.exp(cmath.log(x) / 3)
  return x ** (1/3)