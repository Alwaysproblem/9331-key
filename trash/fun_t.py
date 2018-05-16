import threading as td
import time

def tt(a, delay):
    print("I am the looper." + a)
    time.sleep(delay)

def main():
    t = td.Thread(target=tt, args=['1', 100])
    d = td.Thread(target=tt, args=['2', 2])

    t.start()
    d.start()

    time.sleep(5)

    t._running = False

    d.join()


if __name__ == '__main__':
    main()