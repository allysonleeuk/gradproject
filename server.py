# server = the one receiving the data

import socket

host = "127.0.0.1"
port = 65432 # any number higher than 1023

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    
    
    with conn:
        print(f"Connected by {addr}")
        
        while True:
            user_text = conn.recv(1024)
            
            if not user_text:
                break
            
            print(user_text.decode('utf-8'))

# s.close()

