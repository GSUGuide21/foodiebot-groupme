from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def log(x: number, base: number = math.e) -> number:
  if isinstance(x, complex) or isinstance(base, complex):
      return cmath.log(x, base)
  return math.log(x, base)