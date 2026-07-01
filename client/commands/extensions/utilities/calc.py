from __future__ import annotations
import ast
from dataclasses import dataclass
from io import StringIO
import math
import re
import tokenize

from client.commands.base import Command
from client.parser.arguments import ArgumentParseError, StringArgument
from client.util.math import functions
from client.util.math.operators.binary.add import AddOperator
from client.util.math.operators.binary.bitwise_and import BitwiseAndOperator
from client.util.math.operators.binary.bitwise_or import BitwiseOrOperator
from client.util.math.operators.binary.divide import DivideOperator
from client.util.math.operators.binary.floor_divide import FloorDivideOperator
from client.util.math.operators.binary.left_shift import LeftShiftOperator
from client.util.math.operators.binary.mod import ModulusOperator
from client.util.math.operators.binary.multiply import MultiplyOperator
from client.util.math.operators.binary.power import PowerOperator
from client.util.math.operators.binary.right_shift import RightShiftOperator
from client.util.math.operators.binary.subtract import SubtractOperator
from client.util.math.operators.unary.factorial import FactorialOperator
from client.util.math.operators.unary.invert import InvertOperator
from client.util.math.operators.unary.neg import NegateOperator
from client.util.math.operators.unary.pos import PositiveOperator
from client.util.math.operators.unary.percent import PercentOperator


@dataclass(slots=True)
class _Token:
  kind: str
  value: str


class CalcDomainException(Exception):
  def __init__(self, message):
    super().__init__(f"Domain error: {message}")

class CalcCommand(Command):
  name = "calc"
  aliases = ["calculate"]
  description = "Evaluate a mathematical expression"

  _constants = {
    "e": math.e,
    "inf": math.inf,
    "nan": math.nan,
    "pi": math.pi,
    "tau": math.tau,
    "j": 1j,
  }

  _binary_operators = {
    "|": BitwiseOrOperator(["|"]),
    "&": BitwiseAndOperator(["&"]),
    "<<": LeftShiftOperator(["<<"]),
    ">>": RightShiftOperator([">>"]),
    "+": AddOperator(["+"]),
    "-": SubtractOperator(["-"]),
    "*": MultiplyOperator(["*", "×", "·"]),
    "/": DivideOperator(["/", "÷"]),
    "//": FloorDivideOperator(["//"]),
    "mod": ModulusOperator(["mod"]),
    "^": PowerOperator(["^"]),
    "**": PowerOperator(["^"]),
  }

  _prefix_operators = {
    "+": PositiveOperator(["+"]),
    "-": NegateOperator(["-"]),
    "~": InvertOperator(["~"]),
  }

  _postfix_operators = {
    "!": FactorialOperator(["!"]),
    "%": PercentOperator(["%"]),
  }

  def execute(self, message, context):
    try:
      parsed = message.parse_arguments(StringArgument("expression", greedy=True))
    except ArgumentParseError:
      raise ValueError(f"Usage: {context.prefix}calc <expression>")

    expression = parsed["expression"]
    if not expression:
      raise ValueError(f"Usage: {context.prefix}calc <expression>")

    try:
      # Evaluate the expression using eval in a restricted namespace
      result = self.evaluate(expression)
    except Exception as e:
      raise ValueError(f"Error evaluating expression: {e}")

    return str(result)

  def evaluate(self, expression: str):
    tokens = self._tokenize(self._normalize_expression(expression))
    self._tokens = tokens
    self._current_index = 0

    result = self._parse_bitwise_or()
    self._expect("EOF")
    return result

  def _normalize_expression(self, expression: str) -> str:
    return expression.replace("×", "*").replace("·", "*").replace("÷", "/")

  def _tokenize(self, expression: str) -> list[_Token]:
    tokens: list[_Token] = []
    reader = StringIO(expression).readline
    for token in tokenize.generate_tokens(reader):
      if token.type in {tokenize.NL, tokenize.NEWLINE, tokenize.ENDMARKER}:
        continue
      if token.type == tokenize.NUMBER:
        tokens.append(_Token("NUMBER", token.string))
        continue
      if token.type == tokenize.NAME:
        tokens.append(_Token("NAME", token.string))
        continue
      if token.type == tokenize.OP:
        if token.string in {"(", ")", ",", "+", "-", "*", "/", "//", "%", "^", "**", "!", "&", "|", "<<", ">>", "~"}:
          tokens.append(_Token("OP", token.string))
          continue
        raise ValueError(f"Unsupported operator: {token.string}")
      if token.type == tokenize.ERRORTOKEN and token.string == "!":
        tokens.append(_Token("OP", token.string))
        continue
      if token.type == tokenize.ERRORTOKEN and token.string.strip() == "":
        continue
      raise ValueError(f"Unsupported token: {token.string!r}")

    tokens.append(_Token("EOF", ""))
    return tokens

  def _current(self) -> _Token:
    return self._tokens[self._current_index]

  def _advance(self) -> _Token:
    token = self._current()
    self._current_index += 1
    return token

  def _match(self, kind: str, value: str | None = None) -> bool:
    token = self._current()
    if token.kind != kind:
      return False
    if value is not None and token.value != value:
      return False
    self._advance()
    return True

  def _expect(self, kind: str, value: str | None = None) -> _Token:
    token = self._current()
    if token.kind != kind or (value is not None and token.value != value):
      expected = value if value is not None else kind
      raise ValueError(f"Expected {expected} but found {token.value!r}")
    return self._advance()

  def _parse_bitwise_or(self):
    value = self._parse_bitwise_and()

    while True:
      token = self._current()
      if token.kind == "OP" and token.value == "|":
        self._advance()
        right = self._parse_bitwise_and()
        value = self._binary_operators["|"].execute(value, right)
        continue
      break

    return value

  def _parse_bitwise_and(self):
    value = self._parse_shift()

    while True:
      token = self._current()
      if token.kind == "OP" and token.value == "&":
        self._advance()
        right = self._parse_shift()
        value = self._binary_operators["&"].execute(value, right)
        continue
      break

    return value

  def _parse_shift(self):
    value = self._parse_expression()

    while True:
      token = self._current()
      if token.kind == "OP" and token.value in {"<<", ">>"}:
        self._advance()
        right = self._parse_expression()
        value = self._binary_operators[token.value].execute(value, right)
        continue
      break

    return value

  def _parse_expression(self):
    value = self._parse_term()

    while True:
      token = self._current()
      if token.kind == "OP" and token.value in {"+", "-"}:
        self._advance()
        right = self._parse_term()
        value = self._binary_operators[token.value].execute(value, right)
        continue
      break

    return value

  def _parse_term(self):
    value = self._parse_power()

    while True:
      token = self._current()
      if token.kind == "OP" and token.value in {"*", "/", "//"}:
        self._advance()
        right = self._parse_power()
        operator_value = self._binary_operators[token.value]
        value = operator_value.execute(value, right)
        continue

      if token.kind == "NAME" and token.value == "mod":
        self._advance()
        right = self._parse_power()
        value = self._binary_operators["mod"].execute(value, right)
        continue

      break

    return value

  def _parse_power(self):
    value = self._parse_unary()

    token = self._current()
    if token.kind == "OP" and token.value in {"^", "**"}:
      self._advance()
      right = self._parse_power()
      operator_value = self._binary_operators[token.value]
      return operator_value.execute(value, right)

    return value

  def _parse_unary(self):
    token = self._current()
    if token.kind == "OP" and token.value in {"+", "-", "~"}:
      self._advance()
      operand = self._parse_unary()
      prefix_operator = self._prefix_operators[token.value]
      return prefix_operator.execute(operand)

    return self._parse_postfix()

  def _parse_postfix(self):
    value = self._parse_primary()

    while True:
      token = self._current()
      if token.kind == "OP" and token.value in {"!", "%"}:
        self._advance()
        postfix_operator = self._postfix_operators[token.value]
        value = postfix_operator.execute(value)
        continue
      break

    return value

  def _parse_primary(self):
    token = self._current()

    if token.kind == "NUMBER":
      self._advance()
      return ast.literal_eval(token.value)

    if token.kind == "NAME":
      name = token.value
      self._advance()

      if self._match("OP", "("):
        arguments = []
        if not self._match("OP", ")"):
          while True:
            arguments.append(self._parse_expression())
            if self._match("OP", ","):
              continue
            self._expect("OP", ")")
            break

        function_value = self._resolve_callable(name)
        return function_value(*arguments)

      if name in self._constants:
        return self._constants[name]

      raise ValueError(f"Unknown identifier: {name}")

    if self._match("OP", "("):
      value = self._parse_expression()
      self._expect("OP", ")")
      return value

    raise ValueError(f"Unsupported expression: {token.value!r}")

  def _resolve_callable(self, name: str):
    if hasattr(functions, name):
      candidate = getattr(functions, name)
      if callable(candidate):
        return candidate

    raise ValueError(f"Unknown function: {name}")