import operator
from .base import Operator

class MultiplyOperator(Operator):
  symbols = ['*', '×', '·']

  def execute(self, x, y):
    return operator.mul(x, y)