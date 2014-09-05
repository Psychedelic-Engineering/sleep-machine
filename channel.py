from collections import deque
import math
import numpy as np
from scipy import signal


class Channel:

	def __init__(self, name, min, max, maxNum, offset=0.0):
		self.name = name
		self.min = min
		self.max = max
		self.num = 0
		self.sum = 0
		self.buffersum = 0
		self.size = maxNum
		self.buffer = deque(maxlen=maxNum)
		self.offset = offset

		self.npBufferSize = 800
		self.npBufferPos = 0
		self.npBuffer = np.zeros(self.npBufferSize)

	def __repr__(self):
		return "%s (%.1f-%.1f)" % (self.name, self.min, self.max)

	def calibrate(self):
		self.offset = -self.buffersum / min(self.size, self.num)

	def smooth(self, x,beta):
		window_len=50
		sampleRate = 10
		cutOff = 0.01
		fir_coeff = signal.firwin(window_len, cutOff)
		smoothed = signal.lfilter(fir_coeff, 1.0, self.npBuffer)
		return smoothed

	def putValue(self, value):
		# deque buffer
		if self.num >= self.size:
			self.buffersum -= self.buffer[0]
		newValue = value
		self.buffersum += newValue
		self.buffer.append(newValue)
		self.num += 1
		self.sum += newValue
		"""
		# numpy buffer
		self.npBufferPos += 1
		if self.npBufferPos >= self.npBufferSize:
			self.npBufferPos = 0
			self.smoothed = self.smooth(self.npBuffer, 1)
			self.gradient = np.diff(self.npBuffer)
			try:
				self.onUpdate(self)
			except:
				#raise
				pass
		self.npBuffer[self.npBufferPos] = value
		"""
		# Auto Calibration
		#if self.num % 100 == 0:
		#	self.calibrate()

	def calibrate(self):
		self.offset = -self.buffer[-1]

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

	def getDeriv(self):
		val = self.buffer[-1]                           # current value
		avg = self.buffersum / min(self.size, self.num) # moving average
		mix = 0.5 * val + 0.5 * avg                     # weighted average
		dif = avg - val
		#dif = 5 * math.pow(dif / 20, 6)             # differential
		return dif