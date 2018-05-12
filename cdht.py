#!usr/bin/python3
import sys
import socket
import threading as td
import socketserver
import time
import argparse

def parserArgument():

    parser = argparse.ArgumentParser(description='the assignment of 9331')
    parser.add_argument('peer',type = int, help = 'peer number', action = 'store')
    parser.add_argument('_1st_sucsor',type = int, help = 'the first successor', action = 'store')
    parser.add_argument('_2nd_sucsor',type = int, help = 'the second successor', action = 'store')

    return parser.parse_args()


class Peer(object):
    def __init__(self, peer, first, second, BASE_PORT, IP = '127.0.0.1'):
        self.name = 'peer ' + str(peer)
        self.ip = IP
        self.port = BASE_PORT + peer
        self.host = (self.ip, self.port)
        self.fs = (self.ip, first + BASE_PORT)                 # the first successor host 
        self.fs_name = 'peer ' + str(first)
        self.ss = (self.ip, second + BASE_PORT)                # the second succesor host 
        self.ss_name = 'peer ' + str(second)

    def test(self, succesor):
        # configure the protocol into UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Message = "Ping Message from the " + self.name 
                    # + ' ' + \
                    # self.fs_name if succesor == 'first' else self.ss_name
        data = Message.encode('utf-8')
        if succesor == 'first':
            sock.sendto(data, self.fs)
            print("Sending ping request to the " + self.fs_name)
        elif succesor == 'second':
            sock.sendto(data, self.ss)
            print("Sending ping request to the " + self.ss_name)
        else:
            pass

        received = sock.recv(1024).decode('utf-8')
        # print(received)

        if (received == "Received"):
            print("A ping response message was received from " + (self.fs_name if succesor == 'first' else self.ss_name))
            # pass
        else:
            print("the Wrong ping response received from " + (self.fs_name if succesor == 'first' else self.ss_name))
            # pass
        


# Based on code from Python Docs here: 
# https://docs.python.org/2/library/socketserver.html
# Base Request Handler Doc:
# http://docstore.mik.ua/orelly/other/python/0596001886_pythonian-chp-19-sect-2.html
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
   def handle(self):
        data = self.request[0].decode('utf-8')
        socket = self.request[1]
        print("A ping request message was received from peer " + data.split()[-1] + ".")
        socket.sendto("Received".encode('utf-8'), self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass



def main():
    # Since all UDP listeners are 50000 + ID, here's base port
    BASE_PORT = 50000
    argv = parserArgument()
    p = Peer(argv.peer, argv._1st_sucsor, argv._2nd_sucsor, BASE_PORT)

    server = ThreadedUDPServer(p.host, ThreadedUDPRequestHandler)
    server_thread = td.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread: ", server_thread.name)

    print(f"starting test the successor of the {p.name}")

    check_1 = td.Timer(5, p.test, args=['first'])
    check_2 = td.Timer(5, p.test, args=['second'])

    check_1.start()
    check_2.start()

    # check_1.cancel()
    # check_2.cancel()


if __name__ == '__main__':
    main()
    # threads = []

