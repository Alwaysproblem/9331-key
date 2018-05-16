from cdht import Peer

p = Peer(2, 3, 4, 50000)

host = ('127.0.0.1', 9999)

# p._requestQuit(host)
# print(p.readCommand())

# print(p.File_is_here(2, ))

# import threading as td
# import time as tt
# import sys

# class P:
#     def __init__(self):
#         self.lock = td.Lock()
#         self.shareVar = 0

#     def A(self):
#         for _ in range(10):
#             self.lock.acquire()
#             print(f"the A func is {self.shareVar}")
#             self.shareVar += 1
#             print(f"the A func is {self.shareVar}")
#             self.lock.release()

        
#     def B(self):
#         for _ in range(10):
#             self.lock.acquire()
#             print(f"\t\tthe B func is {self.shareVar}")
#             self.shareVar += 10
#             print(f"\t\tthe B func is {self.shareVar}")
#             self.lock.release()

    

# def main():
#     p = P()
#     thread_pool = [ td.Thread(target=p.A), td.Thread(target=p.B) ]

#     for t in thread_pool:
#         t.start()

#     for t in thread_pool:
#         t.join



# if __name__ == '__main__':
#     main()