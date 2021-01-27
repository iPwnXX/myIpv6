# 需要设置免密， 将public key添加到github上

import os
import git
from git import Repo
import threading,time


class upLoader:
    def __init__(self, cycle_time=60, verbose=False):
        self.git_dir = './'  # 文件位置。
        self.MyIpv6 = ''
        self.keywords = ['IPv6', '2001']
        self.cycleTime = cycle_time  # update period.(in second)
        self.verbose = verbose  # print debug information
        self.lastIpv6 = ''
        self.last_time_upload = '- - - -'
        self.last_time_checked = '- - - -'
        self.infoFuncs = None
        self.initial_start()

    def set_check_period(self, period):
        self.cycleTime = period
        if self.verbose:
            print('check period changes to %i' % self.cycleTime)

    def set_info_funcs(self, funcs):
        self.infoFuncs = funcs

    def get_ipv6_address(self):
        text = os.popen('ipconfig').read()
        lines = text.split('\n')
        for line in lines:
            if self.keywords[0] in line and self.keywords[1] in line:
                self.MyIpv6 = line[line.find('2001'):]
                break
        if self.verbose:
            print('current IPV6:\n', self.MyIpv6)
        self.last_time_checked = time.strftime("%Y-%m-%d %H:%M:%S",
                                               time.localtime())
        if self.infoFuncs is not None:
            self.infoFuncs[0]()

    def write_and_upload(self):
        with open(self.git_dir + 'ipv6.txt', 'w') as f:
            f.write(self.MyIpv6)

        if self.verbose:
            print('try git push...')
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
        if self.infoFuncs is not None:
            self.infoFuncs[1]()

    def check_update(self):
        self.get_ipv6_address()
        if self.MyIpv6 != self.lastIpv6:
            if self.verbose:
                print('different from last ipv6:\n', self.lastIpv6)
            self.write_and_upload()
            self.lastIpv6 = self.MyIpv6
            self.last_time_upload = time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime())

        else:
            if self.verbose:
                print('ipv6 no update')

    def initial_start(self):
        with open(self.git_dir + 'ipv6.txt', 'r') as f:
            self.lastIpv6 = f.read()
            if self.verbose:
                print('saved ipv6:', self.lastIpv6)
        self.timer_task()

    def timer_task(self):
        self.check_update()
        timer = threading.Timer(self.cycleTime, self.timer_task)
        timer.start()


if __name__ == "__main__":
    UpLoader = upLoader(cycle_time=5, verbose=True)

    # break

