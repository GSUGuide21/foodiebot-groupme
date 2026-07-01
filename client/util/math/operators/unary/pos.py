import operator
from .base import Operator

class PositiveOperator(Operator):
  symbols = ['+']

  def execute(self, x):
    return operator.pos(x)