import operator
from .base import Operator

class DivideOperator(Operator):
  symbols = ['/', '÷']

  def execute(self, x, y):
    return operator.truediv(x, y)