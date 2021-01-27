# 需要设置免密， 将public key添加到github上

import os
import git
from git import Repo
import threading


class upLoader:
    def __init__(self, cycle_time=60, verbose=False):
        self.git_dir = './'  # 文件位置。
        self.MyIpv6 = ''
        self.keywords = ['IPv6', '2001']
        self.cycleTime = cycle_time  # update period.(in second)
        self.verbose = verbose  # print debug information
        self.lastIpv6 = ''
        self.timer_task()

    def get_ipv6_address(self):
        text = os.popen('ipconfig').read()
        lines = text.split('\n')
        for line in lines:
            if self.keywords[0] in line and self.keywords[1] in line:
                self.MyIpv6 = line.split('. :')[1]
                break
        if self.verbose:
            print(self.MyIpv6)

    def write_and_upload(self):
        with open(self.git_dir + 'ipv6.txt', 'w') as f:
            f.write(self.MyIpv6)

        dir_file = os.path.abspath(self.git_dir)  #
        repo = Repo(dir_file)
        try:
            g = repo.git
            g.add("--all")
            g.commit("-m auto update")
            g.push()
            if self.verbose:
                print("Successful push!")

        except git.GitCommandError as exc:
            if self.verbose:
                print(exc.stderr)

    def check_update(self):
        self.get_ipv6_address()
        if self.MyIpv6 is not self.lastIpv6:
            self.write_and_upload()
            self.lastIpv6 = self.MyIpv6
        else:
            if self.verbose:
                print('ipv6 no update')

    def timer_task(self):
        #   if execF is False:
        self.check_update()  # 判断任务是否执行过，没有执行就执行

    #     execF=True
    #   else:#任务执行过，判断时间是否新的一天。如果是就执行任务
    #     desTime=time.strftime("%Y-%M-%D",time.localtime())
    #     if desTime > curTime:
    #       execF = False#任务执行执行置值为
    #       curTime=desTime
        timer = threading.Timer(self.cycleTime, self.timer_task)
        timer.start()


if __name__ == "__main__":
    UpLoader = upLoader(cycle_time=20, verbose=True)

    # break

