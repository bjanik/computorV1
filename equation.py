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
				if '*' in value:
					coef = float(value.split('*')[0])
				else:
					split = value.split('X')
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
			for token in token_list:
				if prev_token is not None:
					if (token.kind in ['NUMBER', 'UNKNOWN'] and prev_token.kind in ['NUMBER', 'UNKNOWN']) or token.kind == prev_token.kind:
						error("Parsing error")
					if prev_token.kind == 'OP' and prev_token.value == '-':
						token.coef *= -1
						prev_token.value = '+'
				prev_token = token
			if prev_token.kind == "OP":
				error("Parsing error")

	def reduce_equation(self):
		for power in self.powers_right.keys():
			coef = self.powers_left.get(power)
			if coef is None:
				self.powers_left[power] = self.powers_right[power] * -1
			else:
				self.powers_left[power] -= self.powers_right[power] 

	def print_reduced_equation(self):
		for power, coef in sorted(self.powers_left.items()):
			if power == '0':
				print(coef, end="")
			elif power == '1':
				print("{}*X".format(coef), end="")
			else:
				print("{}*X^{}".format(coef, power), end="")
		print(" = 0")

	def create_dict(self, stack):
		dico = {}
		for token in stack:
			if dico.get(token.power) is None:
				dico[token.power] = token.coef
			else:
				dico[token.power] += token.coef
		for key in list(dico.keys()):
			if dico[key] == 0:
				del dico[key]
		return dico
		
	def solve_equation(self):
		if float(max(self.powers_left.keys())) > 2:
			error("The polynomial degree is stricly greater than 2, I can't solve")
		a = self.powers_left.get(2, 0)
		b = self.powers_left.get(1, 0)
		c = self.powers_left.get(0, 0)
		delta = b**2 - 4 * a * c
		if a:
			if delta == 0:
				x1 = -1 * (b / (2 * a))
				print("Disciminant is 0, unique solution is\n{}".format(x1))
			elif delta > 0:
				x1 = (-1 * b - delta**0.5) / (2 * a)
				x2 = (-1 * b + delta**0.5) / (2 * a)
				print("Disciminant is strictly positive, the two solutions are\n{}\n{}".format(x1, x2))
			else:
				print("Complex solution exists")