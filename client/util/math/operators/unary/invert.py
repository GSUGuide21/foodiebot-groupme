import operator
from .base import Operator

class InvertOperator(Operator):
  symbols = ['~']

  def execute(self, x):
    return operator.invert(x)