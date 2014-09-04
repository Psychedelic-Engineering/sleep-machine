from datetime import datetime, date


def parseTime(strTime):
	return datetime.strptime(strTime, "%H:%M")


def dayTime(dt):
	return replaceDate(dt, date.min)


def replaceDate(dt, newDate=None):
	if newDate is None:
		newDate = datetime.now().date()
	return datetime.combine(newDate, dt.time())

