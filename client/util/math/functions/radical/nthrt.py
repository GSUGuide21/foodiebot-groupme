from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def nthrt(x: number, n: number) -> number:
  if n == 0:
      raise DomainError("Cannot take the zeroth root of a number.")
  if isinstance(x, complex) or x < 0:
      return cmath.exp(cmath.log(x) / n)
  return x ** (1/n)