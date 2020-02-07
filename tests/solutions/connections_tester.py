import socket
import time

s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.google.com", 80))

stop_time: float = time.time() + 0.050
while time.time() < stop_time:
    pass

s.close()
