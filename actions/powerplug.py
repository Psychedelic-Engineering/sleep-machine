import time
from hardware.Adafruit_MCP230xx import Adafruit_MCP230XX

mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)
mcp.config(0, mcp.OUTPUT)
mcp.config(1, mcp.OUTPUT)
mcp.output(0, 0)
mcp.output(1, 0)
time.sleep(2)
mcp.output(0, 1)
mcp.output(1, 1)


def switchRelais():
	logging.info("Alarm")
	mcp.output(0, 0)
	time.sleep(10 * 60)
	mcp.output(1, 0)
	time.sleep(20 * 60)
	mcp.output(0, 1)
	mcp.output(1, 1)
