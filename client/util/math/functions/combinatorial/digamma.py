from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def _digamma_complex(z: complex) -> complex:
  if z.imag == 0 and z.real <= 0 and float(z.real).is_integer():
    raise DomainError("Digamma is undefined for non-positive integers.")

  if z.real < 0.5:
    return _digamma_complex(1 - z) - math.pi / cmath.tan(math.pi * z)

  result = 0j
  while z.real < 8:
    result -= 1 / z
    z += 1

  inverse = 1 / z
  inverse_squared = inverse * inverse

  return (
    result
    + cmath.log(z)
    - 0.5 * inverse
    - inverse_squared * (
      (1 / 12)
      - inverse_squared * (
        (1 / 120)
        - inverse_squared * (
          (1 / 252)
          - inverse_squared * (
            (1 / 240)
            - inverse_squared * (5 / 660)
          )
        )
      )
    )
  )

def digamma(x: number) -> number:
  if isinstance(x, complex):
    return _digamma_complex(x)

  result = _digamma_complex(complex(x, 0))
  if abs(result.imag) > 1e-12:
    return result
  return result.real