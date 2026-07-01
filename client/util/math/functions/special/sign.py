from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def sign(x: number) -> number:
  if isinstance(x, complex):
      return complex(math.copysign(1, x.real), math.copysign(1, x.imag))
  return math.copysign(1, x) if x != 0 else 0