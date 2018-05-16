#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = "127.0.0.1"

port = 50000 + 2

# 绑定端口
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

while True:
    clientsocket,addr = serversocket.accept()

    while True:
        # 建立客户端连接
        # clientsocket,addr = serversocket.accept()

        print("连接地址: %s" % str(addr))

        msg = str(clientsocket.recv(1024), 'utf-8')
        if msg == 'exit':
            break
        print(msg)

    clientsocket.close()