from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError
from .factorial import factorial

import cmath
import math

def npr(n: number, r: number) -> number:
  if not isinstance(n, int) or not isinstance(r, int):
    raise DomainError("n and r must be integers")
  return factorial(n) / factorial(n - r)

permutation = npr