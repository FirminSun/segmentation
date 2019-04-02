import os 


filepath = "/home/chou/data/segment-result/2"


ftxtid = open('./imglist_id.txt', 'w')
cnt=0
typ = ["jpg","JPG"]
for filename,_,imgs in os.walk(filepath):
    for img in imgs:
        if(img.split(".")[-1] not in typ):
           continue
        cnt += 1
        ftxtid.write(img+"\n")
print("total:%d"%cnt)

