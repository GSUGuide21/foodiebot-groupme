import operator
from .base import Operator

class ModulusOperator(Operator):
  symbols = ['mod']

  def execute(self, x, y):
    return operator.mod(x, y)