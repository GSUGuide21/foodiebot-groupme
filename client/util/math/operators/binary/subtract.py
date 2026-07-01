import operator
from .base import Operator

class SubtractOperator(Operator):
  symbols = ['-']

  def execute(self, x, y):
    return operator.sub(x, y)