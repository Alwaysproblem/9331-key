import socket  
  
address = ('127.0.0.1', 50000 + 2)  
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(address)
s.listen(2)

while True:
    clientsocket,addr = s.accept()

    mssg = clientsocket.recv(1024).decode('utf-8')
    print(mssg)

    msg = input("please input message:")
    if not msg:
        break
    clientsocket.send(msg.encode('utf-8'))

s.close()

#  the peer 4 is your second successor!