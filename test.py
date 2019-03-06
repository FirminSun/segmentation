import segmentImage
import SaliencyRC
import cv2
import numpy as np
import random
import os
wid = 360
hei = 252
def Gaussian_Blur(gray):    # 高斯去噪(去除图像中的噪点)
    """
    高斯模糊本质上是低通滤波器:
    输出图像的每个像素点是原图像上对应像素点与周围像素点的加权和

    高斯矩阵的尺寸和标准差:
    (9, 9)表示高斯矩阵的长与宽，标准差取0时OpenCV会根据高斯矩阵的尺寸自己计算。
    高斯矩阵的尺寸越大，标准差越大，处理过的图像模糊程度越大。
    """
    blurred = cv2.GaussianBlur(gray, (9, 9),0)
    return blurred

def Sobel_gradient(blurred): 
    """
        索比尔算子来计算x、y方向梯度
        关于算子请查看:https://blog.csdn.net/wsp_1138886114/article/details/81368890
    """
    gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    return gradX, gradY, gradient
def Thresh_and_blur(gradient):  #设定阈值
    blurred = cv2.GaussianBlur(gradient, (9, 9),0)
    (_, thresh) = cv2.threshold(blurred, 10, 255, cv2.THRESH_OTSU)
    """
    cv2.threshold(src,thresh,maxval,type[,dst])->retval,dst (二元值的灰度图)
    src：  一般输入灰度图
	thresh:阈值，
	maxval:在二元阈值THRESH_BINARY和
	       逆二元阈值THRESH_BINARY_INV中使用的最大值 
	type:  使用的阈值类型
    返回值  retval其实就是阈值 
	"""
    return thresh
def findEdge(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred = Gaussian_Blur(gray)
    gradX, gradY, gradient = Sobel_gradient(blurred)
    thresh = Thresh_and_blur(gradient)
    cv2.imshow("thresh",thresh)
    
    return thresh

def enhaceEdge(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred = Gaussian_Blur(gray)
    gradX, gradY, gradient = Sobel_gradient(blurred)
    thresh = Thresh_and_blur(gradient)
    cv2.imshow("thresh",thresh)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if(thresh[i][j]>10):
                img[i][j][0]=255
                img[i][j][1]=0
                img[i][j][2]=255
    return img


def test_segmentation():
    for filep,_, names in os.walk("../../pz_goods"):
        for imgname in names:
            # if("IMG_0839.JPG" != imgname):
            #     continue
            imgp = os.path.join(filep,imgname)
            img3f = cv2.imread(imgp)
            
            wid = 336
            hei = int((img3f.shape[0]/img3f.shape[1])*wid)
	    
            img3f = cv2.resize(img3f,(wid,hei))
            cv2.imshow("org",img3f)
            img3f = enhaceEdge(img3f)
            cv2.imshow("enhace",img3f)

            img3f = img3f.astype(np.float32)
            img3f *= 1. / 255
            imgLab3f = cv2.cvtColor(img3f,cv2.COLOR_BGR2Lab)
            num,imgInd = segmentImage.SegmentImage(imgLab3f,None,0.5,200,50)

            print(num)
            print(imgInd)
            colors = [[random.randint(0,255),random.randint(0,255),random.randint(0,255)] for _ in range(num)]
            showImg = np.zeros(img3f.shape,dtype=np.uint8)
            height = imgInd.shape[0]
            width = imgInd.shape[1]
            for y in range(height):
                for x in range(width):
                    if imgInd[y,x].all() > 0:
                        if(x==10 or x==wid-10 or y==10 or y==hei-10):
                            f = colors[imgInd[y,x] % num]
                            for i in range(len(colors)):
                                if(f == colors[i]):
                                    colors[i]=[0,0,0]
                           
                        showImg[y,x] = colors[imgInd[y,x] % num]
            cv2.imshow("sb",showImg)
            result= os.path.join("../res-pz","_1_"+imgname)
            cv2.imwrite(result,showImg)

            cv2.waitKey(5)
def test_rc_map():
    for filep,_, names in os.walk("../hardimg"):
        for imgname in names:
            imgp = os.path.join(filep,imgname)
            # img3i = cv2.imread("test.jpg")
            img3i = cv2.imread(imgp)
            img3i = cv2.resize(img3i,(352,352))

            thr = findEdge(img3i)
            cv2.imshow("enhace edge",thr)

            img3f = img3i.astype(np.float32)
            img3f *= 1. / 255
            #sal = SaliencyRC.GetRC(img3f,segK=20,segMinSize=200)
            start = cv2.getTickCount()
            sal = SaliencyRC.GetHC(img3f)
            end = cv2.getTickCount()
            print((end - start)/cv2.getTickFrequency())
            np.save("sal.npy",sal)
            idxs = np.where(sal < (sal.max()+sal.min()) / 1.8)
            img3i[idxs] = 0
            sal = sal * 255
            sal = sal.astype(np.int16)
            cv2.namedWindow("sb")
            cv2.moveWindow("sb",20,20)
            cv2.imshow('sb',sal.astype(np.int8))
            
            cv2.imshow("org ss",img3i)

            for i in range(img3i.shape[0]):
                for j in range(img3i.shape[1]):
                    if(thr[i][j]>10):
                        img3i[i][j][0]=255
                        img3i[i][j][1]=0
                        img3i[i][j][2]=255
            cv2.imshow("ss",img3i)

            result= os.path.join("../res-pz","_1_"+imgname)
            cv2.imwrite(result,img3i)
            # cv2.waitKey(0)

if __name__ == "__main__":
    # np.set_printoptions(threshold=np.nan)
    test_segmentation()
    # test_rc_map()
