import operator
from .base import Operator

class LeftShiftOperator(Operator):
  symbols = ['<<']

  def execute(self, x, y):
    return operator.lshift(x, y)