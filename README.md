# segmentation
### 1. 分割代码
##### 1.1 文件夹：SaliencyRC 实现"Global Contrast based Salient Region Detection"的目标分割方法。
> 代码实现了简单背景下商品识别，实现了"Global Contrast based Salient Region Detection"论文中的方法，效果：对于透明包装商品、饮料瓶处理效果不行。
### 2.1 文件夹: deeplab_for_segment实现deeplabv3商品分割代码
> 用于deeplab模型训练和测试相关代码
### 3.1 文件夹： processTools小工具用于模型输出后处理
> createlist.py用于制作输入的image list文件,模型inference要用到
> process.py完成最大连通域查找，分割图边缘的压缩（缩边），制作用于图像融合要用的样本格式。
> inference.py 用于模型的批量预测,添加batchsize,batchsize>1时保证输入图片尺寸一样

### 2.数据预处理
原始分割数据比较乱，需要做进一步的数据预处理，下面列出预处理操作内容：
##### 2.1 分割数据按SKU存放。
> 说明：将同类商品放置到一个文件夹内，且文件夹以商品标签命名；<br>
> 实现方式：人手操作，按SKU存放；

##### 2.2 检查SKU命名是否正确
> 说明：对文件名称与商品信息总表进行校验，查验SKU命名是否正确
> 实现方式：自行写脚本实现<br>

##### 2.3 重命名待分割图像数据，命名规则
> 说明：对文件夹内的图像进行重命名，命名格式为 {class}_{num}.jpg,其中{class}指代标签，{num}指代自增序号<br>
> 实现方式：脚本操作，执行./data_processing/obj_png_rename.py 即可，执行代码: python obj_png_rename.py --png_path path_to_png_dir_

##### 2.4 分割结果格式化
> 说明1：输出按照SKU存放<br>
> 说明2：输出与输入名称对应，文件格式为png格式<br>
> 实现方式：自己脚本实现

##### 2.5 上传
> 说明1：数据包命名方式为segment_{year}-{month}-{day}_{comment}，其中year/month/day分别为年月日，comment为备注信息<br>
> 说明2：readme，增加readme.txt文件，对数据进行说明<br>
> 说明3：classes，增加classes.txt文件，对数据中的商品类别进行汇总；
> 说明4：数据包需进行压缩成zip后上传；
> 说明5：压缩包与数据包命名需要一致；
> 实现方式：自行编写脚本实现；
