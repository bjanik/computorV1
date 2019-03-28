import sys

def ft_sqrt(number):
    x = number
    i = 0
    error = 0.000001
    while i < number:
        new_x = 0.5 * (x + (number / x))
        if ft_abs(x - new_x) < error:
            return new_x
        x = new_x
        i += 1
    return new_x


# def ft_sqrt(number):
    

def ft_abs(number):
  	if number < 0:
  		return -number
  	return number

def error(message):
	print(message, file=sys.stderr)
	sys.exit(1)