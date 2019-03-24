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
		self.reduced_form = ""
		
	def _initial_checks(self):
		if self.str.count('=') < 1:
			error("Equation does not have '=' sign")
		if self.str.count('=') > 1:
			error("Equation has too much '=' signs")

	def _tokenize(self, string):
		tokens = []
		token_specification = [
		    ("UNKNOWN", r'(\d+(\.\d*)?(\*)?)?[Xx](\^\d+(\.\d*)?)?'),
		    ('NUMBER',  r'\d+(\.\d*)?'),   # Integer or decimal number
		    ('OP',       r'[+\-/*]'),      # Arithmetic operators
		    ('MISMATCH', r'.'),            # Any other character
		]
		tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
		for tok in re.finditer(tok_regex, string):
			kind = tok.lastgroup
			value = tok.group()
			coef = 1
			power = 0
			if kind == 'NUMBER':
				value = float(value) if '.' in value else int(value)
				coef = value
				power = 0
			elif kind == 'MISMATCH':
				error("Error: unrecognized character {}".format(value))
			tokens.append(Token(value, kind, coef, power))
		return tokens