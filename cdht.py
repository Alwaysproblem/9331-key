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


class Peer:
    def __init__(self, peer, first, second, BASE_PORT, IP = '127.0.0.1'):
        self.base_port = BASE_PORT
        self.peerID = peer
        self.name = 'peer ' + str(peer)
        self.ip = IP
        self.port = BASE_PORT + peer
        self.host = (self.ip, self.port)
        self.fs = (self.ip, first + BASE_PORT)                 # the first successor host 
        self.fs_name = 'peer ' + str(first)
        self.ss = (self.ip, second + BASE_PORT)                # the second succesor host 
        self.ss_name = 'peer ' + str(second)
        self.fs_alive = False
        self.ss_alive = False
        self.peer_isAlive = {'first': False, 'second': False}  # the sign flag for receive function
        self.fp = None                                         # first parent
        self.sp = None                                         # second parent

    def peer_recv(self, sock, succesor):
        while True:
            received = sock.recv(1024).decode('utf-8')
            # print(received)
            # print(f"the peer {self.fs_name if succesor == 'first' else self.ss_name} alive is {self.peer_isAlive} in the recv.")
            if (received == (self.fs_name if succesor == 'first' else self.ss_name) + " received"):
                self.peer_isAlive[succesor] = True
                print("A ping response message was received from " + (self.fs_name if succesor == 'first' else self.ss_name))
            else:
                print("the Wrong ping response received from " + (self.fs_name if succesor == 'first' else self.ss_name))
            # time.sleep(0.1)

    def test(self, succesor, recv_timeout):
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
        self.peer_isAlive[succesor] = False
            
        t = td.Thread(target=self.peer_recv, args=[sock, succesor])
        t.setDaemon(True)
        t.start()
        Timer_start = time.time()

        # print(f"the peer alive is {self.peer_isAlive} before the loop")

        while not self.peer_isAlive[succesor] and time.time() - Timer_start < recv_timeout:
            pass
        
        # print(f"the peer alive is {self.peer_isAlive} after the loop")
        print(f"the {(self.fs_name if succesor == 'first' else self.ss_name)} timeout is {time.time() - Timer_start}")


        if self.peer_isAlive[succesor] == True:
            if succesor == 'first':
                self.fs_alive = True
            elif succesor == 'second':
                self.ss_alive = True
        else:
            if succesor == 'first':
                self.fs_alive = 'timeout'
                self.fs, self.fs_alive, self.fs_name = self.ss, self.ss_alive, self.ss_name
                self.ss, self.ss_alive, self.ss_name = None, None, None
                self.RequestSuccessor()
            elif succesor == 'second':
                self.ss_alive = 'timeout'
                self.RequestSuccessor()



    def RequestSuccessor(self):
        sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_TCP.connect(self.fs)

        Message = 'who is your first the succesor?'.encode('utf-8')

        sock_TCP.send(Message)

        recvdata = sock_TCP.recv(1024).decode('utf-8')

        Message = 'exit'.encode('utf-8')
        # recvdata = "the peer {} is your second successor!"

        sock_TCP.sendall(Message)
        SecID = int(recvdata.split()[2])

        self.ss, self.ss_alive, self.ss_name = (self.ip, SecID + self.base_port), True, f"peer {SecID}"

        print(f"{self.ss}")
        print(self.ss_alive)
        print(self.ss_name)

        sock_TCP.shutdown(1)
        sock_TCP.close()

class UDP_Server:
    def __init__(self, host, peerID, mode = 'UDP'):
        self.ip = host[0]
        self.port = host[1]
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peerID = peerID

    def handle(self):
        self.sock.bind(self.host)
        while True:
            data, addr = self.sock.recvfrom(1024)
            data = str(data, 'utf-8')
            print("A ping request message was received from peer " + data.split()[-1] + ".")
            # print(f"peer {self.port} received")
            self.sock.sendto(f"peer {self.peerID} received".encode('utf-8'), addr)


class TCP_Server:
    def __init__(self, host, peerID, mode = 'TCP'):
        self.ip = host[0]
        self.port = host[1]
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peerID = peerID
    
    def handle(self, peer):
        self.sock.bind(self.host)
        self.sock.listen(5)
        while True:
            client_socket, client_addr = self.sock.accept()
            while True:
                data = str(client_socket.recv(1024), 'utf-8')
                if data == 'exit':
                    break
                print(data)
                if data == 'who is your first the succesor?':
                    msg = f"the {peer.fs_name} is your second successor!"
                    client_socket.sendall(bytes(msg, 'utf-8'))
            client_socket.close()
            time.sleep(0.5)



def pingService(peer, timeout, refresh_time):
    while True:
        check_1 = td.Thread(target = peer.test, args=['first', timeout])
        check_2 = td.Thread(target = peer.test, args=['second', timeout])

        check_1.start()
        check_2.start()

        # print(f"the ss states is {peer.ss_alive}")
        # print(f"the fs states is {peer.fs_alive}")

        check_1.join()
        check_2.join()
        time.sleep(refresh_time)



def main():
    # Since all UDP listeners are 50000 + ID, here's base port
    BASE_PORT = 50000
    argv = parserArgument()
    p = Peer(argv.peer, argv._1st_sucsor, argv._2nd_sucsor, BASE_PORT)

    UDPserver = UDP_Server(p.host, p.peerID)
    UDPserve_forever = td.Thread(target = UDPserver.handle)
    UDPserve_forever.setDaemon(True)
    UDPserve_forever.start()

    TCPserver = TCP_Server(p.host, p.peerID)
    TCPserve_forever = td.Thread(target = TCPserver.handle, args=[p])
    TCPserve_forever.setDaemon(True)
    TCPserve_forever.start()


    # setup the UDP Server for ping command
    # UDPserver = ThreadedUDPServer(p.host, ThreadedUDPRequestHandler)
    # UDPserver_thread = td.Thread(target=UDPserver.serve_forever)
    # UDPserver_thread.daemon = True
    # UDPserver_thread.start()
    # print("UDPServer loop running in thread: ", UDPserver_thread.name)

    # setup the TCP Server for 
    # TCPserver = ThreadedUDPServer(p.host, ThreadedTCPRequestHandler)
    # TCPserver_thread = td.Thread(target=)
    # TCPserver_thread.daemon = True
    # TCPserver_thread.start()
    # print("TCPServer loop running in thread: ", TCPserver_thread.name)

    print(f"starting test the successor of the {p.name}")

    time.sleep(0.5)

    ping = td.Thread(target=pingService, args=[p, 2, 10])
    # ping.setDaemon(True)
    ping.start()

    # time.sleep(2)

    # print(f"the fs state is {p.fs_alive}")
    # print(f"the ss state is {p.ss_alive}")

    ping.join()

    # check_1 = td.Thread(target = p.test, args=['first', 2])
    # check_2 = td.Thread(target = p.test, args=['second', 2])

    # check_1.start()
    # check_2.start()
    
    # check_1.join()
    # check_2.join()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)


