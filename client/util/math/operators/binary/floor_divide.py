import operator
from .base import Operator

class FloorDivideOperator(Operator):
  symbols = ['//']

  def execute(self, x, y):
    return operator.floordiv(x, y)