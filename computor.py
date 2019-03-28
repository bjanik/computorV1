#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import re
import sys

from equation import Equation
from token import Token
from utils import error

def create_rpn(tokens):
	op_precedence = {'+': 0, '*': 1}
	output_stack = []
	op_stack = []
	for token in tokens:
		if token.kind == 'OP':
			if len(op_stack) > 0 and op_precedence[op_stack[len(op_stack) - 1].value] > op_precedence[token.value]:
				while (len(op_stack) != 0):
					output_stack.append(op_stack.pop())
			op_stack.append(token)
		elif token.kind in ['NUMBER', 'UNKNOWN']:
			output_stack.append(token)
	while (len(op_stack) != 0):
		output_stack.append(op_stack.pop())
	return output_stack

def resolve_rpn(input_stack):
	stack = []
	for token in input_stack:
		if token.kind in ['NUMBER', 'UNKNOWN']:
			stack.append(token)
		if token.value == '*':
			op1 = stack.pop()
			op2 = stack.pop()
			kind = 'UNKNOWN' if op1.kind == 'UNKNOWN' or op2.kind == 'UNKNOWN' else 'NUMBER'
			power = op1.power + op2.power if op1.coef * op2.coef != 0 else 0 
			tok = Token("", kind, op1.coef * op2.coef, power)
			stack.append(tok)
		elif token.value == '+':
			op1 = stack.pop()
			op2 = stack.pop()
			if op1.kind == op2.kind and op1.power == op2.power:
				tok = Token("", op1.kind, op1.coef + op2.coef, op1.power)
				stack.append(tok)
			else:
				stack.append(op2)
				stack.append(op1)
	return stack

def main():
	if len(sys.argv) == 1:
		error("Missing input")
	eq = Equation(sys.argv[1])
	eq.parse_equation()
	eq.powers_right = eq.create_dict(resolve_rpn(create_rpn(eq.tokens_right)))
	eq.powers_left = eq.create_dict(resolve_rpn(create_rpn(eq.tokens_left)))
	eq.reduce_equation()
	eq.print_reduced_equation()
	eq.solve_equation()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(130)