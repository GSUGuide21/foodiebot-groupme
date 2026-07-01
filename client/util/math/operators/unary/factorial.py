from client.util.math.functions import factorial
from .base import Operator

class FactorialOperator(Operator):
  symbols = ["!"]
  position = "postfix"

  def execute(self, x):
    return factorial(x)