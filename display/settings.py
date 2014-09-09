from gui import GUI, Widget, Slider


class Settings(GUI):

	fontname = 'display/fonts/digital-7.ttf'

	def __init__(self, display):
		GUI.__init__(self, display)

		self.onClose = None
		self.onSetLight = None
		self.lumWarm = 0
		self.lumCold = 0

		self.margin = 8

		self.cellsX = 4
		self.cellsY = 4

		self.gridW = (self.width - self.margin * (self.cellsX + 1)) / self.cellsX
		self.gridH = (self.height - self.margin * (self.cellsY + 1)) / self.cellsY

		nextX = self.margin
		nextY = self.margin

		buttonQuit = Widget(self, nextX, nextX, self.gridW, self.gridH, name="quit", label="Quit")
		nextX += self.gridW + self.margin
		buttonReboot = Widget(self, nextX, nextY, self.gridW, self.gridH, name="reboot", label="Reboot")
		nextX += self.gridW + self.margin
		button3 = Widget(self, nextX, nextY, self.gridW, self.gridH)
		nextX += self.gridW + self.margin
		buttonClose = Widget(self, nextX, nextY, self.gridW, self.gridH, name="close", label="CLOSE")
		sliderWidth = self.gridW * 4 + 3 * self.margin
		nextX = self.margin
		nextY  += self.gridH + self.margin
		sliderWarm = Slider(self, nextX, nextY, sliderWidth, self.gridH, name="warm", label="WARM")
		nextY  += self.gridH + self.margin
		sliderCold = Slider(self, nextX, nextY, sliderWidth, self.gridH, name="cold", label="COLD")

		sliderWarm.onChange = self.changeLight
		sliderCold.onChange = self.changeLight
		buttonQuit.onClick = self.clickButton
		buttonReboot.onClick = self.clickButton
		button3.onClick = self.clickButton
		buttonClose.onClick = self.clickButton

		self.addWidget(buttonQuit)
		self.addWidget(buttonReboot)
		self.addWidget(button3)
		self.addWidget(buttonClose)
		self.addWidget(sliderWarm)
		self.addWidget(sliderCold)

		self.drawBG()

	def changeLight(self, slider, value):
		if slider.name == "warm":
			self.lumWarm = value
		elif slider.name == "cold":
			self.lumCold = value
		if self.onSetLight:
			self.onSetLight(self.lumWarm, self.lumCold)

	def clickButton(self, button):
		if self.onButton:
			self.onButton(button.name)