import operator
from .base import Operator

class BitwiseAndOperator(Operator):
  symbols = ['&', "and"]

  def execute(self, x, y):
    return operator.and_(x, y)