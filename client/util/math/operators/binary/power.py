import operator
from .base import Operator

class PowerOperator(Operator):
  symbols = ['^']

  def execute(self, x, y):
    return operator.pow(x, y)