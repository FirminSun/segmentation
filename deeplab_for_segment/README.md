deeplab v3实现简单背景商品的分割。
训练测试验证集数据，FTP:/segmentation_data/
环境tensorflow1.6+, python3.5

1.训练数据制作:tfrecord数据
python create_pascal_tf_record.py --data_dir DATA_DIR \
                                  --image_data_dir IMAGE_DATA_DIR \
                                  --label_data_dir LABEL_DATA_DIR 
DATA_DIR voc格式数据存放路径，IMAGE_DATA_DIR jpeg原图存放文件夹，LABEL_DATA_DIR png标签图片存放文件夹
详见create_pascal_tf_record.py代码，可以运行run_create_tfrecord.sh脚本执行数据制作

2.模型训练
python train.py --model_dir MODEL_DIR --pre_trained_model PRE_TRAINED_MODEL
PRE_TRAINED_MODEL 为resnet101基础模型(models文件夹)， MODEL_DIR为训练整个模型的checkpoints存放位置，如该位置有有效的
checkpoints训练时将会加载该数据。详细见train.py。

3.模型前向测试测试：
python inference.py --data_dir DATA_DIR \
                    --infer_data_list INFER_DATA_LIST \
                    --model_dir MODEL_DIR 

DATA_DIR:存放voc格式数据目录，INFER_DATA_LIST：测试图片的txt列表，每行为图片名（必须为jpeg格式），MODEL_DIR：模型存放文件。

4.模型验证：
python evaluate.py --help 查看模型验证参数。

目前模型训练状态：

INFO:tensorflow:train_px_accuracy = 0.9951615, learning_rate = 0.004703234, cross_entropy = 0.015337244, train_mean_iou = 0.98572594 (8.319 sec)

测试效果达到预期目标，存在问题：在原图上测试效果较好，将图片缩小测试效果差，主要原因可能是训练样本都为原图，缩小将会影响目标的像素分布。