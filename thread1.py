#!/usr/bin/pyhton
#coding: utf-8

import threading
import time
from random import randint


def customers(event, lists):
    t = threading.current_thread()
    while True:
        event.wait()
        if event.is_set():
            try:
                int = lists.pop()
                print('{0} is customed by {1}'.format(int, t.name))
                event.clear()   #阻塞所有线程
            except IndexError:
                pass


def producer(event, lists):
    t = threading.current_thread()
    while 1:
        int = randint(1, 1000)
        lists.append(int)
        print('{0} is produced by {1}'.format(int, t.name))
        event.set()     #唤醒其他线程
        time.sleep(1)    #没有实际意义，为了结果输出时看的清楚点。

def main():
    threads = []
    lists = []
    event = threading.Event()

    for name in ('customer1', 'customer2'):
        thread = threading.Thread(target=customers, args=(event, lists))
        threads.append(thread)
        thread.start()

    produce_thread = threading.Thread(target=producer, args=(event, lists))
    threads.append(produce_thread)
    produce_thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

