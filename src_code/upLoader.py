# 需要设置免密， 将public key添加到github上

import os
import git
from git import Repo
import threading
import time


class upLoader:
    def __init__(self, git_dir='../../',  cycle_time=60, verbose=False, gui_enable=False):
        self.git_dir = git_dir  # 文件位置。
        self.MyIpv6 = ''
        self.keywords = ['IPv6', '2001']
        self.cycleTime = cycle_time  # update period.(in second)
        self.verbose = verbose  # print debug information
        self.lastIpv6 = ''
        self.last_time_checked = '- - - -'
        self.last_time_upload = '- - - -'
        self.infoFuncs = None
        self.GUIEnable = gui_enable
        self.initial_start()

    def set_check_period(self, period):
        self.cycleTime = period
        if self.verbose:
            print('check period changes to %i' % self.cycleTime)

    def set_info_funcs(self, funcs):
        self.infoFuncs = funcs

    def get_ipv6_address(self):
        text = ''
        try:
            #     with os.popen('ipconfig', "r") as p:
            #         text = p.read()

            import subprocess

            child = subprocess.Popen("ipconfig", shell=True, stdout=subprocess.PIPE)
            out = child.communicate()  # 保存ipconfig中的所有信息

            text = out[0].decode('gbk')
            lines = text.split('\n')
            for line in lines:
                if self.keywords[0] in line and self.keywords[1] in line:
                    self.MyIpv6 = line[line.find('2001'):].split()[0]
                    break
            if self.verbose:
                print('current IPV6:\n', self.MyIpv6)
            self.last_time_checked = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.localtime())
            if self.infoFuncs is not None:
                self.infoFuncs[0]()

        except UnicodeDecodeError:
            if self.verbose:
                print('error read instruction:', text)


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
            self.lastIpv6 = self.MyIpv6
            self.last_time_upload = time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime())

        except git.GitCommandError as exc:
            if self.verbose:
                print('git error:\n%s' % exc.stderr)

        if self.infoFuncs is not None:
            self.infoFuncs[1]()

    def check_update(self):
        self.get_ipv6_address()
        if self.MyIpv6 != '' and self.MyIpv6 != self.lastIpv6:
            if self.verbose:
                print('different from last ipv6:\n', self.lastIpv6)
                # cmp_str(self.MyIpv6, self.lastIpv6)
            self.write_and_upload()

        else:
            if self.verbose:
                print('ipv6 no update')

    def initial_start(self):
        root_text = self.git_dir + 'ipv6.txt'
        if os.path.isfile(root_text):
            with open(root_text, 'r') as f:
                self.lastIpv6 = f.read()
                if self.verbose:
                    print('saved ipv6:', self.lastIpv6)

        self.timer_task(init=True)

    def timer_task(self, init=False):
        if not init:
            self.check_update()
        timer = threading.Timer(self.cycleTime, self.timer_task)
        if self.GUIEnable:
            timer.setDaemon(True)  # close child thread if main thread is closed.
        timer.start()

# debug
# def cmp_str(str1, str2):
#     for i in range(len(str1)):
#         if str1[i] != str2[i]:
#             print('diff:%s, %s, %i' % (str1[i], str2[i], i))


if __name__ == "__main__":
    UpLoader = upLoader(cycle_time=5, verbose=True)


