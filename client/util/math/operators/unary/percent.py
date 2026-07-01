import operator
from .base import Operator

class PercentOperator(Operator):
  symbols = ['%']
  position = 'postfix'  # Percent operator is typically used as a postfix operator

  def execute(self, x):
    return operator.truediv(x, 100)