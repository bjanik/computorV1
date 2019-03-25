import re

from token import Token
from utils import error

class Equation:
	""" Class representing the equation, left side and right side"""

	def __init__(self, string):
		self.str = string.replace(' ', '')
		self.powers_right = {}
		self.powers_left = {}
		self._initial_checks()
		self.str_left = self.str.split('=')[0].strip()
		self.str_right = self.str.split('=')[1].strip()
		if self.str_left == '' or self.str_right == '':
			error("Error: empty side of equation")
		print(self.str_left, '=', self.str_right)
		self.tokens_left = self._tokenize(self.str_left)
		self.tokens_right = self._tokenize(self.str_right)
		
	def _initial_checks(self):
		if self.str.count('=') < 1:
			error("Equation does not have '=' sign")
		if self.str.count('=') > 1:
			error("Equation has too much '=' signs")

	def _tokenize(self, string):
		""" Split equation side into tokens"""
		tokens = []
		token_specification = [
		    ("UNKNOWN", r'(\d+(\.\d*)?(\*)?)?[Xx](\^\d+(\.\d*)?)?'),
		    ('NUMBER',  r'\d+(\.\d*)?'),   # Integer or decimal number
		    ('OP',       r'[+\-*]'),      # Arithmetic operators
		    ('MISMATCH', r'.'),            # Any other character
		]
		tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
		for tok in re.finditer(tok_regex, string):
			kind = tok.lastgroup
			value = tok.group()
			coef = 1.0
			power = 0.0
			if kind == 'UNKNOWN':
				coef = float(value.split('*')[0]) if '*' in value else float(value.split('X')[0])
				power = 1 if '^' not in value else float(value.split('^')[1])
			if kind == 'NUMBER':
				coef = float(value) if '.' in value else int(value)
				power = 0.0
			elif kind == 'MISMATCH':
				error("Error: unrecognized character {}".format(value))
			tokens.append(Token(value, kind, coef, power))
		return tokens

	def reduce_equation(self):
		for power in self.powers_right.keys():
			coef = self.powers_left.get(power)
			if coef is None:
				self.powers_left[power] = self.powers_right[power] * -1
			else:
				self.powers_left[power] -= coef

	def print_reduced_equation(self):
		for power, coef in sorted(self.powers_left.items()):
			if power == '0':
				print(coef, end="")
			elif power == '1':
				print("{}*X".format(coef), end="")
			else:
				print("{}*X^{}".format(coef, power), end="")
		print(" = 0")

	def solve_equation(self):
		a = self.powers_left.get('2', 0)
		b = self.powers_left.get('1', 0)
		c = self.powers_left.get('0', 0)
		delta = b**2 - 4 * a * c
		if delta == 0:
			sol = -1 * (b / (2 * a))

