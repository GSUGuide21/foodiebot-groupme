from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def log10(x: number) -> number:
  if isinstance(x, complex):
      return cmath.log10(x)
  return math.log10(x)