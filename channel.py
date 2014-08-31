
from collections import deque
import math
import numpy as np

class Channel:

	npBufSize = 100

	def __init__(self, name, min, max, maxNum, offset=0):
		self.name = name
		self.min = min
		self.max = max
		self.num = 0
		self.sum = 0
		self.buffersum = 0
		self.size = maxNum
		self.buffer = deque(maxlen=maxNum)
		self.offset = offset
		self.npBuffer = np.zeros(self.npBufSize)
		self.npBufPos = 0
		pass



	def adjustQueue(self, size):
		pass

	def putValue(self, value):
		if self.num >= self.size:
			self.buffersum -= self.buffer[0]
		newValue = value

		self.buffersum += newValue
		self.buffer.append(newValue)
		self.num += 1
		self.sum += newValue
		if self.num == 20:
			pass
			self.offset = -self.sum / self.num
		if (self.num % 1) == 0:
			pass
			#self.offset -= (self.offset + self.sum / self.num) / 10
			#self.offset = - (self.offset + self.sum / self.num)
		#print self.offset
		if self.npBufPos < self.npBufSize:
			self.npBufPos += 1
		else:
			self.npBufPos = 0
			try:
				self.onUpdate(self)
			except:
				pass
		self.npBuffer[self.npBufPos] = newValue


	def getValue(self):
		#if self.num > 0:
		return self.buffer[-1] + self.offset

	def getAvg(self):
		return self.sum / self.num + self.offset

	def getBufferAvg(self):
		try:
			val = self.buffer[-1]                           # current value
			avg = self.buffersum / min(self.size, self.num) # moving average
			mix = 0.5 * val + 0.5 * avg                     # weighted average
			dif = math.pow((val - avg) / 20, 5)             # differential
			rng = 0
			#for i in self.buffer:
			#	rng = max(abs(avg-i), rng)
			#return rng
			return avg + self.offset
			if dif > 50:
				#self.buffersum = val * self.size
				return val + self.offset
			else:
				return avg + self.offset
		except:
			raise

	def getRng(self):
		rng = 0
		der = 0
		avg = self.buffersum / min(self.size, self.num)
		for i in self.buffer:
			#rng = 0.01 * max(pow(avg - i, 4), rng)
			der = der + pow((avg - i) / 4, 2)
			#der = der + abs(avg-i)
		der /= self.size
		return der


	def __repr__(self):
		return "%s (%.1f-%.1f)" % (self.name, self.min, self.max)

	def getDeriv(self):
		val = self.buffer[-1]                           # current value
		avg = self.buffersum / min(self.size, self.num) # moving average
		mix = 0.5 * val + 0.5 * avg                     # weighted average
		dif = avg - val
		#dif = 5 * math.pow(dif / 20, 6)             # differential
		return dif