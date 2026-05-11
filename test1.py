from multiprocessing import Pipe

input = "testing testing"

def transmit_input(child_conn):
    msg = input
    child_conn.send(msg)
    child_conn.close()