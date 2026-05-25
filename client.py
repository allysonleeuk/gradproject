# client = the one sending

import socket
import time

host = "127.0.0.1"
port = 65432

user_input = 'i love'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    
    while True:
        s.send(user_input.encode())
        time.sleep(2) # send every 2 seconds


# NOTE: do I want to code the time interval and changed variable in here 
# OR open and close server after each interval hits to send over current variable