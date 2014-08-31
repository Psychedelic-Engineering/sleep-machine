__author__ = 'makra'

import serial, time, pygame

width = 800
height = 600
colors = (
	(255,0,0),
	(255,255,0),
	(0,255,0),
	(0,255,255),
	(0,0,255),
	(255,0,255),
	(255,255,255),
	(128,0,0),
	(0,128,0),
	(0,0,128),
	(0,128,128)
)

if x >= (width-1):
	x = 0
	surface.fill((0,0,0))
	#self.surface.scroll(-1,0)
	#pygame.draw.rect(self.surface, (0,0,0), (self.width-1, 0, 2, self.height))
	#x = self.width-1
else:
	self.x += 1
for i, value in enumerate(self.values):
	col = self.colors[i]
	min = self.sensor.channels[i].min
	max = self.sensor.channels[i].max
	y = int(self.map_value(value,min,max,self.height,0))
	self.surface.set_at((self.x,y), col)

surface.blit(self.surface, (0,0))

ser = serial.Serial("/dev/cu.usbmodem228731")  # open first serial port
print ser.name          # check which port was really used

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((width, height))


for i in range(10):
	ser.write("!")
	ser.flush()
	result = ser.readline()
	result = floats = [float(x) for x in result.split(",")]
	print result
	time.sleep(1)

ser.close()