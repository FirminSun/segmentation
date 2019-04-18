
from utils import image_utils
from utils import io_utils
import os
import random

def scan_all_file(dir_path):
    file_list = io_utils.scan_all_files(dir_path)
    return file_list

def scan_child_file(dir_path):
    classes = io_utils.scan_child_files(dir_path)
    return classes

def group_image(pool,group_name):
    group_dict = {}
    for fn in pool:
        fn_classes = os.path.split(os.path.dirname(fn))[1]
        if fn_classes not in group_name:
            continue
        if fn_classes in group_dict:
            group_dict[fn_classes].append(fn)
        else:
            group_dict[fn_classes] = [fn]
    return group_dict

def choice_one_png(group):
    output_list = []
    for key in group.keys():
        output_list.append(random.choice(group[key]))
    return output_list

def save_output(output,save_path):
    for fn in output:
        image = image_utils.load_image(fn)
        image = image_utils.resize_image(image, (200,200))
        sp = os.path.join(save_path,os.path.split(os.path.dirname(fn))[1]+ '.png')
        image_utils.save_image(image,sp)

def main(dir_paths):
    for dir_path in dir_paths:
        pool = scan_all_file(dir_path=dir_path)
        group_name = scan_child_file(dir_path)
        group = group_image(pool, group_name)
        output = choice_one_png(group)
        io_utils.mkdir('/home/hyl/data/data-lyl/backend')
        save_output(output, '/home/hyl/data/data-lyl/backend')



if __name__=='__main__':
    # dir_paths = ['/home/hyl/data/ljk/github-pro/zjai-fusion/data/obj_png/obj_png_2018-12-28_600classes',
    #              '/home/hyl/data/ljk/github-pro/zjai-fusion/data/obj_png/obj_png_2018-10-24_136classes',
    #              '/home/hyl/data/ljk/github-pro/zjai-fusion/data/obj_png/obj_png_2018-10-25_150classes',
    #              '/home/hyl/data/ljk/github-pro/zjai-fusion/data/obj_png/obj_png_2018-10-09_169classes']
    dir_paths = ['/home/hyl/data/ljk/github-pro/zjai-fusion/data/obj_png/box_goods_1']
    main(dir_paths)