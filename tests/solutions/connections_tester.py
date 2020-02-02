import socket
import time

s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.google.com", 80))
time.sleep(0.1)
s.close()
