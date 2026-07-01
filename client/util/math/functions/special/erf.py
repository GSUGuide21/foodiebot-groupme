from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import math

_ERF_MAX_TERMS = 200
_ERF_TOLERANCE = 1e-15

def _erf_complex(z: complex) -> complex:
  if z == 0:
    return 0j
  if z.real < 0:
    return -_erf_complex(-z)

  series = z
  term = z
  for index in range(1, _ERF_MAX_TERMS):
    term *= -(z * z) / index
    delta = term / (2 * index + 1)
    series += delta
    if abs(delta) < _ERF_TOLERANCE:
      break

  return (2 / math.sqrt(math.pi)) * series

def erf(x: number) -> number:
  if isinstance(x, complex):
    return _erf_complex(x)
  return math.erf(x)