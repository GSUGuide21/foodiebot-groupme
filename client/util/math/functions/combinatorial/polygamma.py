from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError
from client.util.math.functions.combinatorial.digamma import digamma

import math

_POLYGAMMA_TOLERANCE = 1e-15
_POLYGAMMA_MAX_TERMS = 10000

def _polygamma_complex(order: int, z: complex) -> complex:
  if z.imag == 0 and z.real <= 0 and float(z.real).is_integer():
    raise DomainError("Polygamma is undefined for non-positive integers.")

  if order == 0:
    result = digamma(z)
    return result if isinstance(result, complex) else complex(result, 0)

  factorial_order = math.factorial(order)
  recurrence_factor = (-1) ** (order + 1) * factorial_order

  result = 0j
  while z.real < 8:
    result += recurrence_factor / (z ** (order + 1))
    z += 1

  series = 0j
  for index in range(_POLYGAMMA_MAX_TERMS):
    delta = 1 / ((z + index) ** (order + 1))
    series += delta
    if abs(delta) < _POLYGAMMA_TOLERANCE:
      break

  return result + recurrence_factor * series

def polygamma(order: number, x: number) -> number:
  if not isinstance(order, int):
    raise DomainError("Polygamma order must be a non-negative integer.")
  if order < 0:
    raise DomainError("Polygamma order must be a non-negative integer.")

  result = _polygamma_complex(order, complex(x, 0) if not isinstance(x, complex) else x)
  if isinstance(x, complex) or abs(result.imag) > 1e-12:
    return result
  return result.real