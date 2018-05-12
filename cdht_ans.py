#!/usr/bin/python
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
        socket.sendto("Received".encode('utf-8'), self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

def testSuccessors(peerID,testID):
    # Make sure that it tests multiple times after the first time
    t = threading.Timer(5.0, testSuccessors, args=[peerID, testID])
    t.daemon = True
    t.start()

    # Send the message
    HOST, PORT = "localhost", BASE_PORT + testID
    data = "Ping Request from " + str(peerID)

    # Set up to send message. SOCK_DGRAM is the socket type for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # We don't need to connect because UDP, so let's send
    print("Sending ping request to " + str(testID))
    data += '\n'
    sock.sendto(data.encode('utf-8'), (HOST, PORT))
    received = sock.recv(1024)
    received = received.decode('utf-8')
    if (received == "Received"):
        print("A ping response message was received from peer " + str(testID))
    else:
        print("No ping response received from peer " + str(testID))
        t.cancel()


if __name__ == "__main__":
    # Parsing command line arguments
    peerID = int(sys.argv[1])
    successors = (int(sys.argv[2]), int(sys.argv[3]))
    print("Initialising...")
    print("My ID: " + str(peerID))
    print("1st Successor ID: " + str(successors[0]))
    print("2nd Successor ID: " + str(successors[1]))
    
    # Setting up UDP Server
    print("Setting up UDP Server...")
    HOST, PORT = "localhost", BASE_PORT + peerID

    server = ThreadedUDPServer((HOST,PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread: ", server_thread.name)
    
    # Test sending messages to successors
    print("Starting testing of successors")
    testSuccessors(peerID, successors[0])
    testSuccessors(peerID, successors[1])