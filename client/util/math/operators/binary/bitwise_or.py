import operator
from .base import Operator

class BitwiseOrOperator(Operator):
  symbols = ['|', "or"]

  def execute(self, x, y):
    return operator.or_(x, y)