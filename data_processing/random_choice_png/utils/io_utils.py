#!/usr/bin/env python3
# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @time : 19-1-14
# @Author  : jaykky
# @Software: ZJ_AI
# -----------------------------------------------------
import os

def scan_all_files(dir_path):
    file_list=[]
    for roots,dirs,files in os.walk(dir_path):
        for fn in files:
            file_list.append(os.path.join(roots,fn))
    return file_list

def scan_child_files(dir_path):
    file_list=[]
    for fn in os.listdir(dir_path):
        file_list.append(fn)
    return file_list

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
