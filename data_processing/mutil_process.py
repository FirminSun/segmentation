# -*- coding: utf-8 -*-
# @Time    : 5/31/2018 10:06 AM
# @Author  : sunyonghai
# @File    : preprocess_bg.py
# multiprocessing "handle_background"
# @Software: ZJ_AI
import multiprocessing
import multiprocessing.dummy
import os

import numpy as np


def do_something(i):
    print('do something_{}'.format(i))

# start to process
def process(i):
    do_something(i)


# mutil process
def mutil_process():
    tasks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cpus = os.cpu_count() // 2
    p = multiprocessing.Pool(cpus)
    p.map_async(process, tasks)

    p.close()
    p.join()


# single process
def single_process():
    tasks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for item in tasks:
        process(item)


def main():
    # single_process()
    mutil_process()

# global variable
lock = multiprocessing.Lock()

if __name__ == '__main__':
    main()