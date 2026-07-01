from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def sech(x: number) -> number:
  if isinstance(x, complex):
      return 1 / cmath.cosh(x)
  return 1 / math.cosh(x)