from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def trunc(x: number) -> number:
  if isinstance(x, complex):
      return complex(math.trunc(x.real), math.trunc(x.imag))
  return math.trunc(x)