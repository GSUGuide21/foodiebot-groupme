import operator
from .base import Operator

class BitwiseXorOperator(Operator):
  symbols = ["xor"]

  def execute(self, x, y):
    return operator.xor(x, y)