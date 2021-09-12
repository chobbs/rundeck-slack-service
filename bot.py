#!/usr/bin/python
import time, os, sys
from routing import worker
import datetime


def streamRun():
	try:
		print("Slack Service: (re)initializing stream")
		while(True):
			print("Slack Service: pulse check healthy")
			time.sleep(60)

	except Exception as e:
		print ('Slack Service error: streamRun exception: %s' % e)
		streamRun()

def restartBot():
	python = sys.executable
	os.execl(python, python, * sys.argv)


if __name__=='__main__':
	try:
		worker.start()
		streamRun()

	except Exception as e:
		print('Slack Service error, main exception: %s' % e)
		worker.stop()
		restartBot()

	# Shouldnt get here
	worker.stop()
