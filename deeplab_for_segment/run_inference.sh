#!bin/sh

#python inference.py --data_dir /home/chou/data/obj_png_2018-12-28_600classes/train_img/ \
#    --infer_data_list /home/chou/data/obj_png_2018-12-28_600classes/val_imglist.txt \
#    --model_dir ./model  \

python inference.py --data_dir /home/chou/data/19of300c-dataset/19goods/ \
    --infer_data_list /home/chou/data/19of300c-dataset/train_imglist.txt \
    --model_dir ./jxmodel  \
    --batchsize 1 \
    --output_dir ./inference/19_goods_result/
#python inference.py --data_dir /home/chou/data/my_dataset_voc/my_dataset_voc/JPEGImages/ \
#    --infer_data_list simpletst/cut.txt \
#    --model_dir ./model 