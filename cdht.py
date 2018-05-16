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
        self.fpID = None                                         # first parent
        self.spID = None                                         # second parent
        self.fp_name = None                                         # first parent
        self.sp_name = None                                         # second parent
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
            # print("Sending ping request to the " + self.fs_name)
        elif succesor == 'second':
            sock.sendto(data, self.ss)
            # print("Sending ping request to the " + self.ss_name)
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
        # print(f"the {(self.fs_name if succesor == 'first' else self.ss_name)} timeout is {time.time() - Timer_start}")


        if self.peer_isAlive[succesor] == True:
            if succesor == 'first':
                self.fs_alive = True
            elif succesor == 'second':
                self.ss_alive = True
        else:
            if succesor == 'first':
                self.fs_alive = 'timeout'
                print(f"{self.fs_name} is no longer alive.")
                self.fs, self.fs_alive, self.fs_name = self.ss, self.ss_alive, self.ss_name
                self.ss, self.ss_alive, self.ss_name = None, None, None
                self.RequestSuccessor()
            elif succesor == 'second':
                self.ss_alive = 'timeout'
                print(f"{self.ss_name} is no longer alive.")
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

        print(f"My first successor is now {self.fs_name}.")
        print(f"My second successor is now {self.ss_name}.")

        sock_TCP.shutdown(1)
        sock_TCP.close()

    def refresh_parent(self):
        if self.fpID != None and self.spID != None:
            self.fp_name = 'peer ' + str(self.fpID)
            self.sp_name = 'peer ' + str(self.spID)
            self.fp = (self.ip, self.base_port + self.fpID)
            self.sp = (self.ip, self.base_port + self.spID)

    def validName(self, FileName):
        if len(FileName) == 4 and FileName.isdigit() is True:
            return int(FileName)
        else:
            return None

    def readCommand(self):
        File, Quit, FileName = False, False, None
        # while True:
        console = input()
        if console == 'quit':
            File, Quit, FileName = False, "quit", None
            # print(f"{File}, {Quit}, {FileName}")
            # break
        elif console.split()[0] == 'request':
            File, Quit, FileName = 'File', False, self.validName(console.split()[-1])
            # print(f"{File}, {Quit}, {FileName}")
            # break
        else:
            pass
        return File, Quit, FileName

    def hash_file(self, FileNum):
        FileNum = int(FileNum)
        return FileNum % 256

    def File_is_here(self, parent, FileNum):
        parent = int(parent)
        FileNum = int(FileNum)
        if parent < self.hash_file(FileNum) <= self.peerID:
            return True
        elif parent > self.peerID and FileNum > parent:
            return True
        elif parent > self.peerID and FileNum < self.peerID:
            return True
        else:
            return False

    def requestFile(self, FileNum, sourceID):
        sourceID = int(sourceID)
        FileNum = int(FileNum)
        sock = socket.socket()
        sock.connect(self.fs)
        sock.sendall(bytes(f"File {FileNum} request from peer {sourceID} through {self.peerID}", 'utf-8'))

        # print(f"File request message for {FileNum} has been sent to my successor.")
        time.sleep(0.1)

        sock.sendall('exit'.encode('utf-8'))
        sock.close()


    def _requestQuit(self, host):
        TCP = socket.socket(type=socket.SOCK_STREAM)
        TCP.connect(host)
        while True:
            Msg = f"{self.name} want to leave."
            TCP.sendall(bytes(Msg, 'utf-8'))
            data = TCP.recv(1024).decode('utf-8')

            # print(f"{data}(this should be granted)")

            if data == "granted":
                # the response message should be "granted"
                TCP.sendall("exit".encode('utf-8'))
                break
        TCP.close()

    def requestQuit(self):
        if self.fp != None and self.sp != None:
            fpthread = td.Thread(target=self._requestQuit, args=[self.fp])
            spthread = td.Thread(target=self._requestQuit, args=[self.sp])
            fpthread.start()
            spthread.start()
            fpthread.join()
            spthread.join()

    def RequestFunc(self):
        # func_dic = {'quit' : self.requestQuit, 'File': self.requestFile}
        while True:
            File, Quit, FileName = self.readCommand()
            if Quit == "quit":
                self.requestQuit()
            elif File == "File" and FileName != None:
                print(f"File request message for {FileName} has been sent to my successor.")
                self.requestFile(FileName, self.peerID)
            elif File == "File" and FileName == None:
                print("the file format is not correct.")
            else:
                # sys.exit(0)
                pass

    def print_peer_debug(self):
        print(f"-------the {self.name} first successor {self.fs_name}---------")
        print(f"-------the {self.name} second successor {self.ss_name}--------")
        print(f"-------the {self.name} parents are {(self.fp_name, self.sp_name)}---------")



class UDP_Server:
    def __init__(self, host, peerID):
        self.ip = host[0]
        self.port = host[1]
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peerID = peerID

    def handle(self, peer):
        self.sock.bind(self.host)
        parent_list = []

        while True:
            data, addr = self.sock.recvfrom(1024)
            data = str(data, 'utf-8')
            parent = data.split()[-1]
            print("A ping request message was received from peer " + parent + ".")
            parent_num = int(parent)

            if len(parent_list) < 2:
                if parent_num not in set(parent_list):
                    parent_list.append(parent_num)
                    if len(parent_list) == 2:
                        if {peer.fpID, peer.spID} == set(parent_list):
                            parent_list = []
                        # print(f"******** there is no need to refresh******")
                        else:
                            peer.fpID = parent_list[0]
                            peer.spID = parent_list[1]
                            # print(peer.fpID)
                            # print(peer.spID)
                            peer.refresh_parent()
            else:
                parent_list = []
            self.sock.sendto(f"peer {self.peerID} received".encode('utf-8'), addr)



class TCP_Server:
    def __init__(self, host, peerID):
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
                # print(data)
                if data == 'exit':
                    break
                elif data == 'who is your first the succesor?':
                    msg = f"the {peer.fs_name} is your second successor!"
                    client_socket.sendall(bytes(msg, 'utf-8'))
                elif data.split()[-1] == 'leave.':
                    data = data.split()
                    print(f"Peer {data[1]} will depart from the network.")
                    client_socket.sendall(bytes("granted", 'utf-8'))
                    if 'peer ' + data[1] == peer.fs_name:
                        peer.fs, peer.fs_alive, peer.fs_name = peer.ss, peer.ss_alive, peer.ss_name
                        peer.ss, peer.ss_alive, peer.ss_name = None, None, None
                    peer.RequestSuccessor()
                elif data.split()[0] == 'File':
                    if data.split()[2] == 'request':
                        File_req = data.split()
                        FileNum = File_req[1]
                        sourceID = File_req[5]
                        parent = File_req[-1]
                        # print(FileNum, ' ', sourceID, " ", parent)
                        if int(sourceID) == peer.peerID:
                            print("there is no such file.")
                        elif peer.File_is_here(parent, FileNum) is True:
                            msg = f"File {FileNum} exists in peer {peer.peerID}"

                            print(f"File {FileNum} is here.")

                            sock = socket.socket()
                            sock.connect((peer.ip, peer.base_port + int(sourceID)))
                            sock.sendall(bytes(msg, 'utf-8'))
                            time.sleep(0.5)
                            sock.sendall('exit'.encode('utf-8'))
                            sock.close()
                            
                            print(f"A response message, destined for peer {sourceID}, has been sent.")

                            # print(msg)
                        else:
                            print(f"File {FileNum} is not stored here.")
                            peer.requestFile(FileNum, sourceID)
                            print("File request message has been forwarded to my successor.")
                    elif data.split()[2] == "exists":
                        print(f"Received a response message from peer {data.split()[-1]}, which has the file {data.split()[1]}.")
                else:
                    pass
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
    TIME_OUT = "2s"
    Refresh_Interval = "60s"
    BASE_PORT = 50000
    argv = parserArgument()
    p = Peer(argv.peer, argv._1st_sucsor, argv._2nd_sucsor, BASE_PORT)

    UDPserver = UDP_Server(p.host, p.peerID)
    UDPserve_forever = td.Thread(target = UDPserver.handle, args=[p])
    UDPserve_forever.setDaemon(True)
    UDPserve_forever.start()

    TCPserver = TCP_Server(p.host, p.peerID)
    TCPserve_forever = td.Thread(target = TCPserver.handle, args=[p])
    TCPserve_forever.setDaemon(True)
    TCPserve_forever.start()

    requestThread = td.Thread(target = p.RequestFunc)
    requestThread.start()

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

    # print(f"starting test the successor of the {p.name}")

    time.sleep(0.5)

    ping = td.Thread(
        target=pingService, 
        args=[p, float(TIME_OUT[:-1]), float(Refresh_Interval[:-1])]
    )
    # ping.setDaemon(True)
    ping.start()

    # time.sleep(2)
    # while True:
    #     # p.print_peer_debug()
    #     time.sleep(2)
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


