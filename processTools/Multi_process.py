#!/usr/bin/python3
import time
import process
import multiprocessing
import multiprocessing.dummy
import os
import numpy as np

save_path = "/home/chou/data/19goods_cut"
imagepath = "/home/chou/data/19goods"
labelpath = "/home/chou/data/19goods_result"
typ = ["jpg","JPG","png","PNG"]

# 为线程定义一个函数
def pro_single(labelname):

    print("%d进程->处理%s.."%(os.getpid(),labelname))
    process.process(imagepath,[labelname],save_path)
      

all_list = []
for filep,_,imgs in os.walk(labelpath):
    for img in imgs:
        if(img.split('.')[-1] not in typ):
            continue
        all_list.append(os.path.join(filep,img))
num = len(all_list)





# mutil process
def mutil_process():
    tasks = all_list
    # for im in tasks:
    #     pro_single(im)
    cpus = os.cpu_count()-1
    p = multiprocessing.Pool(cpus)
    p.map_async(pro_single, tasks)

    p.close()
    p.join()



def main():
    # single_process()
    mutil_process()

# global variable
lock = multiprocessing.Lock()

if __name__ == '__main__':
    main()