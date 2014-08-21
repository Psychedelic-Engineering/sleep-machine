import signal
from mainapp import SleepApp

def quitApp(p1, p2):
	global app
	app.quit()

signal.signal(signal.SIGINT, quitApp)
signal.signal(signal.SIGTERM, quitApp)

app = SleepApp()
app.start()