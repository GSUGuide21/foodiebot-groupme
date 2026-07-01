from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def ceil(x: number) -> number:
  if isinstance(x, complex):
      return complex(math.ceil(x.real), math.ceil(x.imag))
  return math.ceil(x)