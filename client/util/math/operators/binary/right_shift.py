import operator
from .base import Operator

class RightShiftOperator(Operator):
  symbols = ['>>']

  def execute(self, x, y):
    return operator.rshift(x, y)