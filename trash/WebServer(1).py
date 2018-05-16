# Sorry sir, the version of python that I used is python 3.6.2
# Python 3.6.2 (v3.6.2:5fd33b5, Aug 21 2017, 04:14:34) [MSC v.1900 32 bit (Intel)] on win32
# written by YONGXI YANG

import sys
import socket
import argparse
import time
import re 


def parserArgument():
    
    parser = argparse.ArgumentParser(description='the Agent of TreasureHunt')
    # parser.add_argument('host',type = str,default = 'localhost',help = 'the IP address of Server',action = 'store')
    parser.add_argument('port',type = int,default = 80,nargs='+',help = 'the port number of Server',action = 'store')
    return parser.parse_args()


def main():
    argv = parserArgument()
    # print(argv.port[0])
    Web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Web.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    HOST = '127.0.0.1'
    Port = argv.port[0]

    Web.bind((HOST,Port))
    Web.listen(1)
    print('Serving HTTP on Port {}'.format(Port))
    
    while True:
        client_connection, _ = Web.accept()

        request = client_connection.recv(1024)
        request_http = request.decode('utf_8')

        if len(request_http) < 2:
            client_connection.sendall("HTTP/1.1 404 Not Found.\r\n\r\n".encode('utf_8'))
            client_connection.close()
            # break

        request_list = request_http.split()[1]
        print(request_http)

        file_name = request_list[1:]
        print("file name:{}\n".format(file_name))

        try:
            with open(file_name,'rb') as f:
                file_content = f.read()

            client_connection.send('HTTP/1.1 200 OK.\r\n\r\n'.encode('utf_8'))      
            client_connection.sendall(file_content)
            time.sleep(2)
            client_connection.close()
            
        except FileNotFoundError:
            client_connection.sendall("HTTP/1.1 404 Not Found.\r\n\r\n".encode('utf_8'))
            time.sleep(2)
            client_connection.close()

    Web.close()


if __name__ == '__main__':
    main()
