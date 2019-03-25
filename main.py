#!/usr/local/bin/python3
import re
import sys

from equation import Equation
from utils import error

def main():
	if len(sys.argv) == 1:
		error("Missing input")
	eq = Equation(sys.argv[1])
	# for token in eq.tokens_left:
	# 	print(token.kind, token.value)
	# for token in eq.tokens_right:
	# 	print(token.kind, token.value)
	for token_list in [eq.tokens_left, eq.tokens_right]:
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
	for token in eq.tokens_left:
		print(token.value, token.coef, token.power)

def rpn(eq):
	op_precedence = {'+': 0, '*': 1}
	output_stack = []
	op_stack = []
	for token in eq.tokens_left:
		if token.kind == 'OP':
			if len(op_stack) > 0 and op_stack[len(op_stack) - 1]
			op_stack.append(token)
		elif token.kind in ['NUMBER', 'UNKNOWN']:
			output_stack.append(token)

if __name__ == "__main__":
	main()