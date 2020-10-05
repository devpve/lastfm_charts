import datetime
import time

def convert_date(dt):
	dt = datetime.datetime(int(dt[:4]), int(dt[5:7]), int(dt[8:10]), int(dt[11:13]), int(dt[14:16]))
	dt = str(time.mktime(dt.timetuple()))
	return dt[:-2]

