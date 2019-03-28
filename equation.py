import re

from token import Token
from utils import *

class Token:
	def __init__(self, value, kind, coef=1, power=0):
		self.value = value
		self.kind = kind
		self.coef = coef
		self.power = power

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
		# print(self.str_left, '=', self.str_right)
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
		    ('OP',       r'[+\-*]'),       # Arithmetic operators
		    ('MISMATCH', r'.'),            # Any other character
		    ('SKIP', r' \t'),
		]
		tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
		for tok in re.finditer(tok_regex, string):
			kind = tok.lastgroup
			value = tok.group()
			coef = 1.0
			power = 0.0
			if kind == 'SKIP':
				continue
			if kind == 'UNKNOWN':
				if '*' in value:
					coef = float(value.split('*')[0])
				else:
					split = value.split('X') if 'X' in value else value.split('x')
					coef = 1 if split[0] == '' else float(split[0])
				power = 1 if '^' not in value else float(value.split('^')[1])
			if kind == 'NUMBER':
				coef = float(value) if '.' in value else int(value)
				power = 0.0
			elif kind == 'MISMATCH':
				error("Error: unrecognized character {}".format(value))
			tokens.append(Token(value, kind, coef, power))
		return tokens

	def parse_equation(self):
		for token_list in [self.tokens_left, self.tokens_right]:
			prev_token = None
			todel = -1
			for count,token in enumerate(token_list):
				if prev_token is not None:
					if (token.kind in ['NUMBER', 'UNKNOWN'] and prev_token.kind in ['NUMBER', 'UNKNOWN']) or token.kind == prev_token.kind:
						error("Parsing error")
					if prev_token.kind == 'OP' and prev_token.value == '-':
						token.coef *= -1
						prev_token.value = '+'
				prev_token = token
				if count == 0:
					if prev_token.value == '*':
						error("Parsing error")
					if prev_token.kind == 'OP':
						todel = count
						if prev_token.value == '-':
							token.coef *= -1
			if prev_token.kind == "OP":
				error("Parsing error")
			if todel > -1:
				del token_list[todel]

	def reduce_equation(self):
		for power in self.powers_right.keys():
			coef = self.powers_left.get(power)
			if coef is None:
				self.powers_left[power] = self.powers_right[power] * -1
			else:
				self.powers_left[power] -= self.powers_right[power]
		for key in list(self.powers_left.keys()):
			if self.powers_left[key] == 0.0:
				del self.powers_left[key]

	def print_reduced_equation(self):
		print("Reduced equation: ", end="")
		for power, coef in sorted(self.powers_left.items()):
			if power == 0:
				print(coef, end="")
			elif power == 1:
				if power != min(self.powers_left.keys()) and coef > 0:
					print('+', end="")
				if coef == -1:
					print('-', end="")
				elif coef != 1:
					print(coef, end="")
				print("X", end="")
			else:
				if power != min(self.powers_left.keys()) and coef > 0:
					print('+', end="")
				if coef == -1:
					print('-', end="")
				elif coef != 1:
					print(coef, end="")
				if coef != 0:
					print("X^{}".format(power), end="")
		if len(self.powers_left.keys()) == 0:
			print("0X", end="")
		print(" = 0")

	def create_dict(self, stack):
		dico = {}
		for token in stack:
			if dico.get(token.power) is None:
				dico[token.power] = token.coef
			else:
				dico[token.power] += token.coef
		return dico
		
	def solve_equation(self):
		for key in self.powers_left.keys():
			if key > 2:
				error("The polynomial degree is stricly greater than 2, I can't solve")
			if key not in [0, 1, 2]:
				error("Cannot solve equation of degree {}".format(key))
		a = self.powers_left.get(2, 0)
		b = self.powers_left.get(1, 0)
		c = self.powers_left.get(0, 0)
		delta = b**2 - 4 * a * c
		print("a = {}".format(a))
		print("b = {}".format(b))
		print("c = {}".format(c))
		if a != 0:
			print("Calculating discriminant delta = b^2 - 4ac = {}".format(delta))
		if a:
			if delta == 0:
				x1 = (b / (2 * a))
				if x1 != 0:
					x1 *= -1
				print("Discriminant is 0, unique solution is\n{}".format(x1))
			elif delta > 0:
				sqrt = ft_sqrt(delta)
				x1 = (-1 * b - sqrt) / (2 * a)
				x2 = (-1 * b + sqrt) / (2 * a)
				print("Discriminant is strictly positive, the two solutions are\n{}\n{}".format(x1, x2))
			else:
				sqrt = ft_sqrt(ft_abs(delta))
				z_b = -b / (2 * a)
				z1 = -sqrt / (2 * a)
				z2 = sqrt / (2 * a)
				print("Discriminant is strictly negative, the two complex solutions are\n{}".format(z_b), end="")
				print("{0:+}i".format(z1))
				print("{}".format(z_b), end="")
				print("{0:+}i".format(z2))
		else:
			if b == 0 and c == 0:
				print("All real numbers are solutions")
			elif b == 0:
				error("This is nonsense")
			else:
				print("The polynomial degree is one, unique solution is\n{}".format(-1 * c / b))