from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def coth(x: number) -> number:
  if isinstance(x, complex):
      return 1 / cmath.tanh(x)
  return 1 / math.tanh(x)