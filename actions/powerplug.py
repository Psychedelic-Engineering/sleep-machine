import time


class PowerPlug:

	mcp230xx = None

	@classmethod
	def init(cls):
		from hardware.Adafruit_MCP230xx import Adafruit_MCP230XX
		cls.mcp230xx = Adafruit_MCP230XX(busnum=1, address=0x20, num_gpios=16)
		cls.mcp230xx.config(0, cls.mcp230xx.OUTPUT)
		cls.mcp230xx.config(1, cls.mcp230xx.OUTPUT)

		cls.relaisOn(0)
		cls.relaisOn(1)
		time.sleep(2)
		cls.relaisOff(0)
		cls.relaisOff(1)

	@classmethod
	def switchRelais(cls, relais, state):
		cls.mcp230xx.output(relais, state)

	@classmethod
	def relaisOn(cls, relais):
		cls.switchRelais(relais, 0)

	@classmethod
	def relaisOff(cls, relais):
		cls.switchRelais(relais, 1)

	@classmethod
	def alarm(cls):
		cls.relaisOn(0)
		time.sleep(10 * 60)
		cls.relaisOn(1)
		time.sleep(20 * 60)
		cls.relaisOff(0)
		cls.relaisOff(1)
