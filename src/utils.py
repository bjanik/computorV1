import sys

def ft_sqrt(number):
    x = 1
    i = 0
    while i < number:
        x = 0.5 * (x + (number / x))
        i += 1
    return x

def ft_abs(number):
  	if number < 0:
  		return -number
  	return number

def error(message):
	print(message, file=sys.stderr)
	sys.exit(1)