from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def _chypot(x: complex, y: complex) -> number:
  return cmath.sqrt(x * x + y * y)

def hypot(x: number, y: number) -> number:
  if isinstance(x, complex) or isinstance(y, complex):
    return _chypot(x, y)
  return math.hypot(x, y)