# 需要设置免密， 将public key添加到github上

import os
from git import Repo
import threading,time

git_dir = './' # 文件位置。
MyIpv6 = ''
keywords = ['IPv6','2001']

curTime=time.strftime("%Y-%M-%D",time.localtime())#记录当前时间
execF=False
cycleTime = 60  # update period.(in second)

def getIPv6Address():
    global MyIpv6
    text = os.popen('ipconfig').read()
    lines = text.split('\n')
    for line in lines:
        if keywords[0] in line and keywords[1] in line:
            MyIpv6 = line.split('. :')[1]


def writeAndUpload():
    with open(git_dir+'ipv6.txt', 'w') as f:
        f.write(MyIpv6)

    dirfile = os.path.abspath(git_dir) # 
    repo = Repo(dirfile)
    
    g = repo.git
    g.add("--all")
    g.commit("-m auto update")
    g.push()
    print("Successful push!")

def Update():
    getIPv6Address()
    writeAndUpload()

def timerTask():
  global execF
  global curTime
#   if execF is False:
  Update()#判断任务是否执行过，没有执行就执行
#     execF=True
#   else:#任务执行过，判断时间是否新的一天。如果是就执行任务
#     desTime=time.strftime("%Y-%M-%D",time.localtime())
#     if desTime > curTime:
#       execF = False#任务执行执行置值为
#       curTime=desTime
  timer = threading.Timer(cycleTime,timerTask)
  timer.start()

if __name__ == "__main__":
  timer = threading.Timer(cycleTime,timerTask)
  timer.start()
            # break 
    
