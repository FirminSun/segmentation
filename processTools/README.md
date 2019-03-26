# 小工具用于模型输出后处理
## createlist.py用于制作输入的image list文件,模型inference要用到
## process.py完成最大连通域查找，分割图边缘的压缩（缩边），制作用于图像融合要用的样本格式。
## inference.py 用于模型的批量预测,添加batchsize,batchsize>1时保证输入图片尺寸一样
## utils.py 包括基本的图像增强函数，如中值滤波，高斯滤波。包括图像后处理函数如腐蚀、膨胀等。封装了glabcut分割函数。寻找轮廓及最小外接矩形裁剪函数。
