class Token:
	def __init__(self, value, kind, coef=1, power=0):
		self.value = value
		self.kind = kind
		self.coef = coef
		self.power = power
		