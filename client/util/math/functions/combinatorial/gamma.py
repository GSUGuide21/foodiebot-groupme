from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

_LANCZOS_G = 7
_LANCZOS_COEFFICIENTS = (
  0.9999999999998099,
  676.5203681218851,
  -1259.1392167224028,
  771.3234287776531,
  -176.6150291621406,
  12.507343278686905,
  -0.13857109526572012,
  9.984369578019572e-6,
  1.5056327351493116e-7,
)

def _gamma_complex(z: complex) -> complex:
  if z.real < 0.5:
    return math.pi / (cmath.sin(math.pi * z) * _gamma_complex(1 - z))

  z_minus_one = z - 1
  series = _LANCZOS_COEFFICIENTS[0]
  for index, coefficient in enumerate(_LANCZOS_COEFFICIENTS[1:], start=1):
    series += coefficient / (z_minus_one + index)

  t = z_minus_one + _LANCZOS_G + 0.5
  return cmath.sqrt(2 * math.pi) * (t ** (z_minus_one + 0.5)) * cmath.exp(-t) * series

def gamma(x: number) -> number:
  if isinstance(x, complex):
    if x.imag == 0 and x.real <= 0 and float(x.real).is_integer():
      raise DomainError("Gamma is undefined for non-positive integers.")
    return _gamma_complex(x)
  return math.gamma(x)