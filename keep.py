import time
import datetime
import os
import subprocess
while True:
    print(datetime.datetime.now())
    task = subprocess.Popen(r"bash -c 'cd /Users/lizytalk/Projects/talk/ && (git add source && git commit -m update&& git push   \|\& tee -a hexo.log)'", shell=True)
    task.wait()
    time.sleep(60)
