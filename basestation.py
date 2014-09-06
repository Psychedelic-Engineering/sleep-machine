
class LED:

	def __init__(self, device):
		self.initialized = False
		self.device = device

	def cie1931(self, lum):
		lum *= 100.0
		if lum <= 8:
			return lum / 902.3
		else:
			return ((lum + 16.0) / 116.0) ** 3

	def setLight(self, warm, cold):
		cmd = "w %f c %f\n" % (warm, cold)
		self.device.sendQuick(cmd)

	def setLum(self, warm, cold):
		self.setLight(self.cie1931(warm), self.cie1931(cold))