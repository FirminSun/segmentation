import cv2  
import os  
import numpy as np
from skimage.measure import label

save_path = "./png"
imagepath = "/home/chou/data/obj_png_2018-12-28_600classes/imgjpeg"
labelpath = "/home/chou/code/deeplab_v3/tensorflow-deeplab-v3/dataset/deeplab_v3_pred_752"
# 查找最大连通区域
# cv2.namedWindow("orgimg",0)

def erode(img, kernel_size = 3):
    kernel = np.ones((kernel_size,kernel_size),np.uint8)    
    erodeimg = cv2.erode(img,kernel,iterations = 3)
    # cv2.imshow("after erode",erodeimg)
    return erodeimg

# 查找最大连通区域
def largestConnectComponent(bw_img):
    labeled_img, num = label(bw_img, neighbors=8, background=0, return_num=True)    
    # plt.figure(), plt.imshow(labeled_img, 'gray')
    max_label = 0
    max_num = 0
    for i in range(0, num):
        if np.sum(labeled_img == i) > max_num:
            max_num = np.sum(labeled_img == i)
            print(max_num)
            max_label = i
    lcc = (labeled_img == max_label)
    # print(labeled_img.shape)
    retimg = np.zeros(lcc.shape[0:2], dtype=np.uint8)
    retimg[np.where(lcc==False)]=254

    # for i in range(labeled_img.shape[0]):
    #     for j in range(labeled_img.shape[1]):
    #         if(lcc[i][j]):
    #             bw_img[i][j]=0
    #         else:
    #             bw_img[i][j]=254

    
    return retimg

endtyp = ""
typ = ["jpg","JPG","png","PNG"]
imglist=[]
for filep,_,imgs in os.walk(imagepath):
    for img in imgs:
        if(img.split('.')[-1] not in typ):
            continue
        endtyp=img[-4:]
        imglist.append(img[0:-4])

#cv2.namedWindow("orgimg",0)
#cv2.namedWindow("labelimg",0)
cnt=0

for filep,_,imgs in os.walk(labelpath):
    for img in imgs:
        if(img.split('.')[-1] not in typ):
            continue
        if(img[0:-9] not in imglist):
            print("%s中不存在%s..."%(imagepath,img[0:-4]))
            continue

        cnt+=1
        print("%d,process:%s..."%(cnt,img))

        
        labeldata = cv2.imread(os.path.join(filep,img)) 
        i=0
        h = i//labeldata.shape[1]
        w = i%labeldata.shape[1]
        while(labeldata[h][w][0]==255 and labeldata[h][w][1]==255 and labeldata[h][w][2]==255):
            i+=1
            h = i//labeldata.shape[1]
            w = i%labeldata.shape[1]
        print("h and w is:%d,%d..."%(w,h))
        
        j=labeldata.shape[1]*labeldata.shape[0]-1
        h1 = j//labeldata.shape[1]
        w1 = j%labeldata.shape[1]
        while(labeldata[h1][w1][0]==255 and labeldata[h1][w1][1]==255 and labeldata[h1][w1][2]==255):
            j-=1
            h1 = j//labeldata.shape[1]
            w1 = j%labeldata.shape[1]
        print("tesfsgg",labeldata.shape[0]-h1, labeldata.shape[1]-w1)
        labeldata = labeldata[h:h1, w:w1]
        # cv2.imshow("cut",labeldata)
        print("h and w is:%d,%d..."%(w1,h1))
        

        imgdata = cv2.imread(os.path.join(imagepath,img[0:-9]+endtyp),-1)
       
        
        #cv2.imshow("img",labeldata)

        sha = (labeldata.shape[1],labeldata.shape[0])
        if(labeldata.shape != imgdata.shape):
            #labeldata = cv2.resize(labeldata, sha )
            imgdata = cv2.resize(imgdata, sha )
        print(labeldata.shape,imgdata.shape)

        
       
        #find edge-----------------------------
        howImg = np.zeros((labeldata.shape[0],labeldata.shape[1],4),dtype=np.uint8) 
        howImg[:,:,0:3] = imgdata.copy()
        templ = labeldata[:,:,0]+labeldata[:,:,1]+labeldata[:,:,2]
        #查找最大的连通区域：
        templ = largestConnectComponent(templ)
        # cv2.imshow("tes",templ)
        #图像缩边
        templ = erode(templ)

        ind = np.where(templ>0)
        inde = (ind[0], ind[1], np.array(len(ind[0])*[3]) )
        howImg[inde] = 255

        imgclspath = os.path.join(save_path,img.split("_")[0])
        if(not os.path.exists(imgclspath)):
            os.mkdir(imgclspath)
        clspath = os.path.join(imgclspath,img[0:-3]+"png")
        cv2.imwrite(clspath,howImg,[int(cv2.IMWRITE_PNG_COMPRESSION)] )
        # cv2.waitKey()
     


 






