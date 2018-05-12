#!usr/bin/python3
import sys
import socket
import threading
import socketserver
import time

# Since all UDP listeners are 50000 + ID, here's base port
BASE_PORT = 50000

# Based on code from Python Docs here: 
# https://docs.python.org/2/library/socketserver.html
# Base Request Handler Doc:
# http://docstore.mik.ua/orelly/other/python/0596001886_pythonian-chp-19-sect-2.html
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
   def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("A ping request message was received from " + str(data).split()[-1] + ".")
        socket.sendto("Received", self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def testsuccessor(PeerID, testID):
    pass


# def responsetest():
#     pass

# def main():
#     pass


if __name__ == '__main__':
    # main()
    threads = []

