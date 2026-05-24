# client = the one sending

import socket

host = "127.0.0.1"
port = 65432

user_input = 'i love'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    
    # s.sendall(b"Hello world") # b indicates that the string will be sent in 8 bit units
    s.send(user_input.encode())
    
# s.close()
