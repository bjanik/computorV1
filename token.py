class Token:
	def __init__(self, value, kind, coef=None, power=None):
		self.value = value
		self.kind = kind
		self.coef = coef
		self.power = power
		