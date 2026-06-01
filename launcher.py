#IMPORTS
import subprocess
import time

# launcher.py: a more streamlined way to open the files
subprocess.Popen(["python3", "bot.py"])

time.sleep(2)

subprocess.Popen(["python3", "human.py"])