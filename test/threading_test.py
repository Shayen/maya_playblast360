# threading test

import threading, math

# print threading.currentThread()

def run():

	thread = []
	for i in range(100):

		doCompute(i)
	# 	t = threading.Thread(target = doCompute, args = (i,) )
	# 	thread.append(t)

	# for t in thread :
	# 	t.start()

def doCompute(input):

	pass
	print math.tan( math.sin(input) *5 )

if __name__ == '__main__':
		run()	