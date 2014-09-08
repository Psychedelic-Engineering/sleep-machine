from gui import GUI, Widget, Slider


class Settings(GUI):

	fontname = 'display/fonts/digital-7.ttf'

	def __init__(self, display):
		GUI.__init__(self, display)
		self.lumWarm = 0
		self.lumCold = 0

		size = 36

		buttonClose = Widget(self, 2,2,size*2,size, name="close", label="CLOSE")
		sliderWarm = Slider(self, 2,42,316,size, name="warm", label="WARM")
		sliderCold = Slider(self, 2,82,316,size, name="cold", label="COLD")

		sliderWarm.onChange = self.changeLight
		sliderCold.onChange = self.changeLight
		buttonClose.onClick = self.close

		self.addWidget(buttonClose)
		self.addWidget(sliderWarm)
		self.addWidget(sliderCold)

		self.addWidget(Widget(self, 82,2,size*2,size))
		self.addWidget(Widget(self, 162,2,size*2,size))
		self.addWidget(Widget(self, 242,2,size*2,size))

		self.drawBG()

	def changeLight(self, slider, value):
		if slider.name == "warm":
			self.lumWarm = value
		elif slider.name == "cold":
			self.lumCold = value
		try:
			self.onSetLight(self.lumWarm, self.lumCold)
		except:
			pass

	def close(self, button):
		print "Click:"
		try:
			self.onClose()
		except:
			pass