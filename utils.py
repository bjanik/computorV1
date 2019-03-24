import sys

def error(message):
	print(message, file=sys.stderr)
	sys.exit(1)