# launcher.py: a more streamlined way to open the files

import subprocess
import time

subprocess.Popen(["python3", "bot.py"])

time.sleep(2)

subprocess.Popen(["python3", "human.py"])