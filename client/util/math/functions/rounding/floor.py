from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def floor(x: number) -> number:
  if isinstance(x, complex):
      return complex(math.floor(x.real), math.floor(x.imag))
  return math.floor(x)