import time
import datetime
import os
import subprocess
while True:
    print(datetime.datetime.now())
    task = subprocess.Popen(r"bash -c 'cd /Users/lizytalk/Projects/talk/ && (hexo generate \|\& tee -a hexo.log)'", shell=True)
    task.wait()
    task = subprocess.Popen(r"bash -c 'cd /Users/lizytalk/Projects/talk/ && (hexo deploy   \|\& tee -a hexo.log)'", shell=True)
    task.wait()
    time.sleep(60)
