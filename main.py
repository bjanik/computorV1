#!/usr/bin/python3
import re
import sys

from equation import Equation
from utils import error

def main():
	if len(sys.argv) == 1:
		error("Missing input")
	eq = Equation(sys.argv[1])
	for token in eq.tokens_left:
		print(token.kind, token.value)
	for token in eq.tokens_right:
		print(token.kind, token.value)

if __name__ == "__main__":
	main()