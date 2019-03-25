# segmentation
## 文件夹：SaliencyRC 实现"Global Contrast based Salient Region Detection"的目标分割方法。
代码实现了简单背景下商品识别，实现了"Global Contrast based Salient Region Detection"论文中的方法，效果：对于透明包装商品、饮料瓶处理效果不行。
## 文件夹: deeplab_for_segment实现deeplabv3商品分割代码
用于deeplab模型训练和测试相关代码
## 文件夹： processTools小工具用于模型输出后处理
createlist.py用于制作输入的image list文件,模型inference要用到
process.py完成最大连通域查找，分割图边缘的压缩（缩边），制作用于图像融合要用的样本格式。
inference.py 用于模型的批量预测,添加batchsize,batchsize>1时保证输入图片尺寸一样
