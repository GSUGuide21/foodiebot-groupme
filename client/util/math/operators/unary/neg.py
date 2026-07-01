import operator
from .base import Operator

class NegateOperator(Operator):
  symbols = ['-']

  def execute(self, x):
    return operator.neg(x)