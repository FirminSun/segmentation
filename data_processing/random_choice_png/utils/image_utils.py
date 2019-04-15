#!/usr/bin/env python3
# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @time : 19-1-14
# @Author  : jaykky
# @Software: ZJ_AI
# -----------------------------------------------------

import cv2

def load_image(fp):
    return cv2.imread(fp,cv2.IMREAD_UNCHANGED)

def save_image(image,fp):
    cv2.imwrite(fp,image)

def resize_image(image,size):
    image = cv2.resize(image,size)
    return image