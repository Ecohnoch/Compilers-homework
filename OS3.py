class Process(object):
	def __init__(self):
		self.name = "process"
		self.arriveTime = 0
		self.exeTime = 0
		self.startTime = 0
		self.endTime = 0

		self.waitTime = 0
		self.zhouzhuanTime = 0
		self.jiaquanZhouzhuanTime = 0
		self.finish = False


def sortQueue(queue):
	queue.sort(key = lambda d: d.exeTime)



processQueue = []
allProcess = []
allArriveTime = [0, 1, 2, 3, 6, 7, 9, 11, 12, 13, 14, 20, 23, 24, 25, 26]
allExeTime = [1, 35, 10, 5, 9, 21, 35, 23, 42, 1, 7, 5, 3, 22, 31, 1]
for i in range(16):
	tmp = Process()
	tmp.name = i
	tmp.arriveTime = allArriveTime[i]
	tmp.exeTime = allExeTime[i]
	allProcess.append(tmp)

def judgeQuit(allProcess):
	for eachProcess in allProcess:
		if eachProcess.finish == False:
			return True
	return False

def sjf():
	print("tag:  name, startTime, endTime, zhouzhuanTime, jiaquanZhouzhuanTime")
	now = 0
	processQueue.append(allProcess[0])
	while(judgeQuit(allProcess)):
		while(len(processQueue) != 0):
			processQueue[0].startTime = now
			processQueue[0].waitTime = processQueue[0].startTime - processQueue[0].arriveTime
			now = now + processQueue[0].exeTime
			processQueue[0].endTime = now
			processQueue[0].finish = True
			processQueue[0].zhouzhuanTime = processQueue[0].endTime - processQueue[0].arriveTime
			processQueue[0].jiaquanZhouzhuanTime = processQueue[0].zhouzhuanTime * 1.0 / processQueue[0].exeTime
			print("SJF: ", processQueue[0].name, processQueue[0].startTime, processQueue[0].endTime, processQueue[0].zhouzhuanTime, processQueue[0].jiaquanZhouzhuanTime)
			processQueue.pop(0)
		for eachProcess in allProcess:
			if eachProcess.arriveTime <= now and eachProcess.finish == False:
				processQueue.append(eachProcess)
		sortQueue(processQueue)

sjf()
waitAverTime = 0
jiaquanZhouzhuanAverTime = 0
for i in allProcess:
	waitAverTime = waitAverTime + i.waitTime
	jiaquanZhouzhuanAverTime = jiaquanZhouzhuanAverTime + i.jiaquanZhouzhuanTime
print("Wait average time:", waitAverTime * 1.0 / 16)
print("Jiaquan Zhouzhuan average time: ", jiaquanZhouzhuanAverTime * 1.0 / 16)

def FCFS():
	now = 0
	for eachProcess in allProcess:
		eachProcess.startTime = now
		now = now + eachProcess.exeTime
		eachProcess.endTime = now
		eachProcess.waitTime = eachProcess.startTime - eachProcess.arriveTime
		eachProcess.zhouzhuanTime = eachProcess.endTime - eachProcess.arriveTime
		eachProcess.jiaquanZhouzhuanTime = eachProcess.zhouzhuanTime * 1.0 / eachProcess.exeTime
		eachProcess.finish = True
		print("FCFS: ", eachProcess.name, eachProcess.startTime, eachProcess.endTime, eachProcess.zhouzhuanTime, eachProcess.jiaquanZhouzhuanTime)


FCFS()
waitAverTime = 0
jiaquanZhouzhuanAverTime = 0
for i in allProcess:
	waitAverTime = waitAverTime + i.waitTime
	jiaquanZhouzhuanAverTime = jiaquanZhouzhuanAverTime + i.jiaquanZhouzhuanTime
print("Wait average time:", waitAverTime * 1.0 / 16)
print("Jiaquan Zhouzhuan average time: ", jiaquanZhouzhuanAverTime * 1.0 / 16)
