#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys
import time

# def client(ip, port, message):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((ip, port))
#     sock.sendall(bytes(message, 'ascii'))
#     print(message)
#     response = str(sock.recv(1024), 'ascii')
#     # print("Received: {}".format(response))

# def main():
#     BASE_PORT = 50000
#     peerID = 4
#     port = BASE_PORT + peerID
#     while True:
#         client('127.0.0.1', port, 'send message to' + str(('127.0.0.1', port)))
#         time.sleep(1)

# if __name__ == '__main__':
#     main()


# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = "127.0.0.1"

# 设置端口好
port = 9999

# 连接服务，指定主机和端口
s.connect((host, port))

# 接收小于 1024 字节的数据
for i in range(1):
    # Msg = 'send Message to ' + str((host, port))
    Msg = input("please input the message:")
    s.sendall(bytes(Msg, 'utf-8'))
    if Msg == 'exit':
        break
    print(Msg)
    time.sleep(1)

s.shutdown(1)
s.close()