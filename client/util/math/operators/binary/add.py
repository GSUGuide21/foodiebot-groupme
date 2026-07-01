import operator
from .base import Operator

class AddOperator(Operator):
  symbols = ['+']

  def execute(self, x, y):
    return operator.add(x, y)