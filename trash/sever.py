import socket
import SockTimeout as ST

address = ('127.0.0.1', 31500)  
s = ST.SockRecvTimeout(socket.AF_INET, socket.SOCK_DGRAM)  
# s.bind(address)
  
while True:  
    data, timeout = s.recvTimeout(1024, 5, 0.1)
    if not data and timeout != True:
        print("client has exist")  
        break  
    elif timeout == True:
        print("timeout")
        # break
    else:
        print("received:" + data.decode('utf-8'))

s.close()