import os,threading,time
curTime=time.strftime("%Y-%M-%D",time.localtime())#记录当前时间
execF=False
ncount=0
def execTask():
  #具体任务执行内容
  print("execTask executed!")
def timerTask():
  global execF
  global curTime
  global ncount
#   if execF is False:
#     execTask()#判断任务是否执行过，没有执行就执行
#     execF=True
#   else:#任务执行过，判断时间是否新的一天。如果是就执行任务
#     desTime=time.strftime("%Y-%M-%D",time.localtime())
#     if desTime > curTime:
#       execF = False#任务执行执行置值为
#       curTime=desTime
  ncount = ncount+1
  timer = threading.Timer(5,timerTask)
  timer.start()
  print("定时器执行%d次"%(ncount))
if __name__=="__main__":
  timer = threading.Timer(5,timerTask)
  timer.start()