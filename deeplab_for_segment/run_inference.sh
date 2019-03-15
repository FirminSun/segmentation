#!bin/sh

#python inference.py --data_dir /home/chou/data/obj_png_2018-12-28_600classes/train_img/ \
#    --infer_data_list /home/chou/data/obj_png_2018-12-28_600classes/val_imglist.txt \
#    --model_dir ./model  \

python inference.py --data_dir /home/chou/data/pz_goods/ \
    --infer_data_list simpletst/pz.txt \
    --model_dir ./modelnew  \
#python inference.py --data_dir /home/chou/data/my_dataset_voc/my_dataset_voc/JPEGImages/ \
#    --infer_data_list simpletst/cut.txt \
#    --model_dir ./model 