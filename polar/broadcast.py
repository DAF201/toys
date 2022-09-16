import socket
import time
import os
import sys
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
port = 1081
start_time = time.time()
while(1):
    server.sendto(b'', ('<broadcast>', port))
    time.sleep(3)
    if time.time()-start_time > (15*60):
        os.system('python3.8 '+sys.argv[0])
