#!bin/sh

python create_pascal_tf_record.py --data_dir /home/chou/data/obj_png_2018-12-28_600classes \
    --train_data_list /home/chou/data/obj_png_2018-12-28_600classes/train_list.txt \
    --valid_data_list /home/chou/data/obj_png_2018-12-28_600classes/val_list.txt  \
    --image_data_dir imgjpeg \
    --label_data_dir labels.2 \
    --output_path datasetnew