from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

_HURWITZ_ZETA_TOLERANCE = 1e-15
_HURWITZ_ZETA_MAX_TERMS = 64

def _is_non_positive_integer(x: complex) -> bool:
  return x.imag == 0 and x.real <= 0 and float(x.real).is_integer()

def _hurwitz_zeta_complex(s: complex, a: complex) -> complex:
  if s == 1:
    raise DomainError("Hurwitz zeta has a pole at s = 1.")
  if _is_non_positive_integer(a):
    raise DomainError("Hurwitz zeta is undefined for non-positive integer a.")
  if s.real <= 1:
    raise DomainError("Hurwitz zeta currently requires Re(s) > 1 for convergence.")

  total = 0j
  for n in range(_HURWITZ_ZETA_MAX_TERMS):
    delta = 1 / ((a + n) ** s)
    total += delta
    if abs(delta) < _HURWITZ_ZETA_TOLERANCE:
      break

  q = a + _HURWITZ_ZETA_MAX_TERMS
  tail = (
    (q ** (1 - s)) / (s - 1)
    + 0.5 * (q ** -s)
    + (s / 12) * (q ** (-s - 1))
    - (s * (s + 1) * (s + 2) / 720) * (q ** (-s - 3))
    + (s * (s + 1) * (s + 2) * (s + 3) * (s + 4) / 30240) * (q ** (-s - 5))
  )

  return total + tail

def hurwitz_zeta(s: number, a: number) -> number:
  result = _hurwitz_zeta_complex(
    s if isinstance(s, complex) else complex(s, 0),
    a if isinstance(a, complex) else complex(a, 0),
  )
  if isinstance(s, complex) or isinstance(a, complex) or abs(result.imag) > 1e-12:
    return result
  return result.real