import cv2  
import os  
import numpy as np
from skimage.measure import label


def erode(img, kernel_size = 11):
    kernel = np.ones((kernel_size,kernel_size),np.uint8)    
    erodeimg = cv2.erode(img,kernel,iterations = 4)
    # #cv2.imshow("after erode",erodeimg)
    return erodeimg

# 查找最大连通区域
def largestConnectComponent(bw_img):
    bw_img[np.where(bw_img>0)]=254
    
    # cv2.imshow("before",bw_img)
    labeled_img, num = label(bw_img, neighbors=4, background=0, return_num=True) 
    # cv2.imshow("labeled_img",labeled_img)
    # #print(num,"ge")
    if(num<2):
        return bw_img
    max_label = 0
    max_num = 0
    for i in range(1, num+1):
        # img=np.zeros(labeled_img.shape,np.uint8)
        # img[np.where(labeled_img == i)] = 255
        # cv2.imshow("test",img)
        # cv2.waitKey()
        if np.sum(labeled_img == i) > max_num:
            max_num = np.sum(labeled_img == i)
            # #print("max num:",max_num)
            max_label = i
    lcc = (labeled_img == max_label)
    # #print("max label is:",max_label)
    retimg = np.zeros(lcc.shape[0:2], dtype=np.uint8)
    retimg[np.where(lcc==True)]=254
    # for i in range(labeled_img.shape[0]):
    #     for j in range(labeled_img.shape[1]):
    #         if(lcc[i][j]):
    #             retimg[i][j]=254
    #         else:
    #             retimg[i][j]=0

    # cv2.imshow("after",retimg)
    # cv2.waitKey()
    return retimg
        
#空洞填充,适用于物品无靠近边缘！！！！
def fillhole(binary_input):
    h1, w1 = binary_input.shape[:2]
    binary_img = np.zeros((h1+2,w1+2),np.uint8)
    #cv2.imshow("orgimg", binary_input)

    binary_img[1:h1+1,1:w1+1] = binary_input.copy()
    #cv2.imshow("pad edge", binary_img)
    h, w = binary_img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    # #print(mask.shape)
   
    cv2.floodFill(binary_img, mask, (0,0), 254)
    #cv2.imshow("FILL", binary_img)

    binary_img_inv = cv2.bitwise_not(binary_img)
    binary_img_inv = binary_img_inv[1:h1+1,1:w1+1]
    #cv2.imshow("holes", binary_img_inv)
    # #print(np.where(binary_img_inv>200))
    binary_input[np.where(binary_img_inv>200)]=254
    #cv2.imshow("Floodfilled Image", binary_input)
    #cv2.waitKey()
    
    #cv2.waitKey(0)
    return binary_input
#去锯齿
def median(img,thr):
    img_r = cv2.medianBlur(img,thr)
    return img_r

def approxPoly(binary_input, eps = 0.001):
    im = np.zeros(binary_input.shape[:2], dtype="uint8")
    contours, hierarchy = cv2.findContours(binary_input,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    
    for i in range(length):
        cnt = contours[i]
        epsilon = eps * cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.fillPoly(im, [approx], 255)
    return im

endtyp = ".jpg"
typ = ["jpg","JPG","png","PNG"]

def process(imagepath,labellist,save_path):
    if(not os.path.exists(save_path)):
        os.mkdir(save_path)
    cnt=0
    for label in labellist:
        img = label.split("/")[-1]
        filep = label.split(img)[0]

        if(img.split('.')[-1] not in typ):
            continue
        orgimgpath = os.path.join(imagepath,img[0:-9]+endtyp)
        if(not os.path.exists(orgimgpath)):
            #print("%s中不存在%s..."%(imagepath,orgimgpath))
            continue
        cnt+=1
        #print("%d,process:%s..."%(cnt,img))
        labeldata = cv2.imread(os.path.join(filep,img)) 
        # #cv2.imshow("cut",labeldata)
        #print("h and w is:%d,%d..."%(w1,h1))
        imgdata = cv2.imread(orgimgpath,-1)
    
        ##cv2.imshow("img",labeldata)

        sha = (imgdata.shape[1],imgdata.shape[0])
        if(labeldata.shape != imgdata.shape):
            labeldata = cv2.resize(labeldata, sha,interpolation=cv2.INTER_LANCZOS4 )
            # imgdata = cv2.resize(imgdata, sha )
        #print(labeldata.shape,imgdata.shape)

        
    
        #find edge-----------------------------
        howImg = np.zeros((labeldata.shape[0],labeldata.shape[1],4),dtype=np.uint8) 
        howImg[:,:,0:3] = imgdata.copy()
        templ = labeldata[:,:,0]+labeldata[:,:,1]+labeldata[:,:,2]
        #查找最大的连通区域：
        templ = largestConnectComponent(templ)
        # #cv2.imshow("tes",templ)
        #空洞填充,适用于物品无靠近边缘
        templ = fillhole(templ)
        # templ = approxPoly(templ, eps = 0.002)
        templ = median(templ,31)
        #图像缩边
        templ = erode(templ)

        ind = np.where(templ>0)
        if(len(ind[0])>0):
            inde = (ind[0], ind[1], np.array(len(ind[0])*[3]) )
            howImg[inde] = 255

        imgclspath = os.path.join(save_path,img.split("_")[0])
        if(not os.path.exists(imgclspath)):
            os.mkdir(imgclspath)
        clspath = os.path.join(imgclspath,img[0:-3]+"png")
        cv2.imwrite(clspath,howImg,[int(cv2.IMWRITE_PNG_COMPRESSION)] )

def process1(mask_img,imgdata,save_path,imgname):
    if(not os.path.exists(save_path)):
        os.mkdir(save_path)
    labeldata = mask_img
    sha = (imgdata.shape[1],imgdata.shape[0])
    if(labeldata.shape != imgdata.shape):
        labeldata = cv2.resize(labeldata, sha,interpolation=cv2.INTER_LANCZOS4 )
        # imgdata = cv2.resize(imgdata, sha )
    #print(labeldata.shape,imgdata.shape)

    

    #find edge-----------------------------
    howImg = np.zeros((labeldata.shape[0],labeldata.shape[1],4),dtype=np.uint8) 
    howImg[:,:,0:3] = imgdata.copy()
    templ = labeldata[:,:,0]+labeldata[:,:,1]+labeldata[:,:,2]
    #查找最大的连通区域：
    templ = largestConnectComponent(templ)
    # #cv2.imshow("tes",templ)
    #空洞填充,适用于物品无靠近边缘
    templ = fillhole(templ)
    # templ = approxPoly(templ, eps = 0.002)
    templ = median(templ,31)
    #图像缩边
    templ = erode(templ)

    ind = np.where(templ>0)
    if(len(ind[0])>0):
        inde = (ind[0], ind[1], np.array(len(ind[0])*[3]) )
        howImg[inde] = 255

    imgclspath = os.path.join(save_path,imgname.split("_")[0])
    if(not os.path.exists(imgclspath)):
        os.mkdir(imgclspath)
    clspath = os.path.join(imgclspath,imgname[0:-3]+"png")
    cv2.imwrite(clspath,howImg,[int(cv2.IMWRITE_PNG_COMPRESSION)] )      


    






