from multiprocessing import Process, Pipe
from human import transmit_input

while True:
    if __name__ == '__main__':
        parent_conn,child_conn = Pipe()
        p = Process(target=transmit_input, args=(child_conn,))
        p.start()
        print(parent_conn.recv())
