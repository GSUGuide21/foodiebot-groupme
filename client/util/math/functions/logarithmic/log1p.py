from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def log1p(x: number) -> number:
  if isinstance(x, complex):
    return cmath.log(1 + x)
  return math.log1p(x)