import socket
import threading as td
import time

class SockRecvTimeout(socket.socket):
    def __init__(self,family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto=0, fileno=None)
        self.recv_flag = False
        self.recv_data = None
        # self.addr = None
        self.RecvTimeout = False
    
    def _recv(self, buff_size):
        self.recv_data = self.recv(buff_size)
        self.recv_flag = True

    def _recvTimeout(self, buff_size, Timeout, sample_interval):
        t = td.Thread(target=self._recv, args=[buff_size])
        t.setDaemon(True)
        t.start()
        self.recv_flag = False
        self.RecvTimeout = False

        Tstart = time.clock()
        while not self.recv_flag and time.clock() - Tstart < Timeout:
            time.sleep(sample_interval)

        if self.recv_flag == True:
            self.RecvTimeout = False
        else:
            self.RecvTimeout = True
    
    def recvTimeout(self, buff_size, Timeout, sample_interval):
        """
        buff_size refer to the buffer size
        Timeout refer to the timeout
        sample_interveal refer to the interval of 
        """
        t = td.Thread(target=self._recvTimeout, args=[buff_size, Timeout, sample_interval])
        t.start()
        t.join()

        return self.recv_data, self.RecvTimeout
        # return self.recv_data, self.addr, self.RecvTimeout
