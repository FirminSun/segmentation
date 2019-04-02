"""Run inference a DeepLab v3 model using tf.estimator API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os,cv2
import sys
import time
import tensorflow as tf
import zipfile
import deeplab_model
from utils import preprocessing
from utils import dataset_util
import process
from PIL import Image
import matplotlib.pyplot as plt
import configparser
from tensorflow.python import debug as tf_debug
import send_email as SE
import ftp_upload as FU
<<<<<<< HEAD
import ftp_utils

parser = argparse.ArgumentParser()
parser.add_argument('--download_test_data_path', type=str, default="no",
                    help='whether download test images from tfp: [yes, no]')
parser.add_argument('--zip_send_path', type=str, default="no",
=======

parser = argparse.ArgumentParser()
parser.add_argument('--zip_send_email', type=str, default="no",
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107
                    help='whether zip result send to ftp and send notice email: [yes, no]')
parser.add_argument('--save_mask', type=str, default="yes",
                    help='whether save mask of result: [yes, no]')
parser.add_argument('--batchsize', type=int, default=2,
                    help='The batchsie of testing')
parser.add_argument('--data_dir', type=str, default='/home/chou/data/segment-result/2/',
                    help='The directory containing the image data.')

parser.add_argument('--output_dir', type=str, default='./inference/inference_output',
                    help='Path to the directory to generate the inference results')

parser.add_argument('--infer_data_list', type=str, default='./inference/imglist_id.txt',
                    help='Path to the file listing the inferring images.')

parser.add_argument('--model_dir', type=str, default='./jxmodel',
                    help="Base directory for the model. "
                         "Make sure 'model_checkpoint_path' given in 'checkpoint' file matches "
                         "with checkpoint name.")

parser.add_argument('--base_architecture', type=str, default='resnet_v2_101',
                    choices=['resnet_v2_50', 'resnet_v2_101'],
                    help='The architecture of base Resnet building block.')

parser.add_argument('--output_stride', type=int, default=16,
                    choices=[8, 16],
                    help='Output stride for DeepLab v3. Currently 8 or 16 is supported.')

parser.add_argument('--debug', action='store_true',
                    help='Whether to use debugger to track down bad values during training.')

<<<<<<< HEAD
parser.add_argument('--num_classes', type=int, default=2,
                    help='numble of classes.')
=======
_NUM_CLASSES = 2
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107

def get_setting_cfg():
  filename="./config.cfg"
  with open(filename, 'r') as fr:
    cfg = configparser.configparser()
    cfg.readfp(fr)
  # 读取所有sections：
  secs = cfg.sections()         # ['TRAIN', 'TEST']
  print (secs)
  return

def get_zip_file(input_path, result):
    """
    对目录进行深度优先遍历
    :param input_path:
    :param result:
    :return:
    """
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)
 
 
def zip_file_path(input_path, output_path, output_name):
    """
    压缩文件
    :param input_path: 压缩的文件夹路径
    :param output_path: 解压（输出）的路径
    :param output_name: 压缩包名称
    :return:
    """
    if(not(input_path and output_path and output_name)):
      print("zip error")
      return
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    get_zip_file(input_path, filelists)
    i=0
    total = len(filelists)
    for file in filelists:
        sys.stdout.write('zip {0}/%s\r'.format(i + 1)%total)
        i+=1
        sys.stdout.flush()
        f.write(file)
    # 调用了close方法才会保证完成压缩
    f.close()
    return output_path + r"/" + output_name

<<<<<<< HEAD
def zip_and_set_email(filedir, remote_path_u):
  # #压缩
  time_str = time.strftime('%Y-%m-%d',time.localtime(time.time()))
  # print(time_str)
  zip_name = "seg_"+time_str+"_service.zip"
  if(filedir[-1]=='/'):
    filedir=filedir[:-1]
  zip_path = filedir.split(filedir.split('/')[-1])[0]
  zip_file_path(filedir, zip_path, zip_name)
  #发送到ftp
  print("now send to tfp...")
  FU.run_upload(remote_path_u, os.path.join(zip_path,zip_name) )
  #发送邮件  
  print("now send email...")
  content = "hi all!\n"+ \
            "segmentation result data has uploaded to ftp server address:" \
=======
def zip_and_set_email(filedir):
  #压缩
  time_str = time.strftime('%Y-%m-%d',time.localtime(time.time()))
  print(time_str)
  zip_name = "seg_"+time_str+"_service.zip"
  zip_file_path(filedir, './', zip_name)
  #发送到ftp
  remote_path_u = "/segmentation_data/test_result/"
  FU.run_upload(remote_path_u,os.getcwd()+"/"+zip_name)
  #发送邮件  
  content = "hi all!\n"+ \
            "segmentation data has uploaded to ftp server address:" \
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107
            +remote_path_u+zip_name+", thank you!"
  SE.notify(content)
  return True

def main(unused_argv):
  # Using the Winograd non-fused algorithms provides a small performance boost.
  os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'

  pred_hooks = None
  if FLAGS.debug:
    debug_hook = tf_debug.LocalCLIDebugHook()
    pred_hooks = [debug_hook]

  model = tf.estimator.Estimator(
      model_fn=deeplab_model.deeplabv3_model_fn,
      model_dir=FLAGS.model_dir,
      params={
          'output_stride': FLAGS.output_stride,
          'batch_size': FLAGS.batchsize,  # Batch size must be 1 because the images' size may differ
          'base_architecture': FLAGS.base_architecture,
          'pre_trained_model': None,
          'batch_norm_decay': None,
<<<<<<< HEAD
          'num_classes': FLAGS.num_classes,
=======
          'num_classes': _NUM_CLASSES,
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107
      })
  image_files = []

  if(FLAGS.infer_data_list != "none"):
    examples = dataset_util.read_examples_list(FLAGS.infer_data_list)
    for filename in examples:
      if(filename[-3:] in ["jpg","JPG"]):
        image_file = os.path.join(FLAGS.data_dir,filename) 
      else:
        image_file = os.path.join(FLAGS.data_dir,filename+".jpg") 
      # print("\n\n\n",filename)
      # print(FLAGS.data_dir,filename)
      # print(image_file)
      image_files.append(image_file)
  else:
    for filename,_,imgs in os.walk(FLAGS.data_dir):
      for img in imgs:
        if(img[-3:] in ["jpg","JPG"]):
          image_files.append(os.path.join(filename,img))
        else:
          print("file type error:%s..."%img)


  predictions = model.predict(
        input_fn=lambda: preprocessing.eval_input_fn(image_files,None,batch_size=FLAGS.batchsize),
        hooks=pred_hooks)

  output_dir = FLAGS.output_dir
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  for pred_dict, image_path in zip(predictions, image_files):
    image_basename = os.path.splitext(os.path.basename(image_path))[0]
    
    print("generating for:", image_path)

    mask = pred_dict['decoded_labels']
    if(FLAGS.save_mask == "yes"):
      output_mask = image_basename + '_mask.png'
      path_to_mask = os.path.join(output_dir, output_mask)
      cv2.imwrite(path_to_mask,mask)
    orgdata = cv2.imread(image_path)
    process.process1(mask,orgdata,output_dir,image_path.split('/')[-1])
<<<<<<< HEAD

    if(FLAGS.zip_send_path != "no"):
      zip_and_set_email(FLAGS.output_dir, FLAGS.zip_send_path)

def download_test_data(remote_path,local_path):
    print("now down load images form ftp...")
    if(not os.path.exists(local_path)):
      os.mkdir(local_path)
    ftp = ftp_utils.ftp_handler()
    result = ftp_utils.download(
        ftp=ftp,
        remote_path=remote_path,
        localAbsDir=local_path
    )
    print("all completed" if result[0] == 1 else "some failed")
    print(result[1])
    if(remote_path.split('.')[-1] == 'zip'):
      print("now unzip file...")
      local_zip = os.path.join(local_path,remote_path.split('/')[-1])
      f = zipfile.ZipFile(local_zip,'r')
      for file in f.namelist():
        f.extract(file,local_path)
    return
=======
    
    
    
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107

def load_setting_cfg(args):
    filename="./config.cfg"
    if(not os.path.exists(filename)):
      print("file config.cfg not exist! will run default configue"%filename)
      return

    with open(filename, 'r') as fr:
        cfg = configparser.ConfigParser()
        cfg.readfp(fr)
    # 读取所有sections：
    secs = cfg.sections()         # ['TRAIN', 'TEST']
    args_dict = args.__dict__
    # ops0 = dict(cfg.items(secs[0]))      #options of ['TRAIN'] 
    ops1 = dict(cfg.items(secs[1]))      #options of ['TEST'] 
    # for k,v in ops0.items():
    #     if k in args_dict.keys():
    #         args_dict[k] = v
    for k,v in ops1.items():
        if k in args_dict.keys():
            args_dict[k] = type(args_dict[k])(v)
<<<<<<< HEAD
=======

>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107
    return


if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)
  FLAGS, unparsed = parser.parse_known_args()
  #用配置文件config.cfg中的覆盖配置
  load_setting_cfg(FLAGS)
<<<<<<< HEAD
  if(FLAGS.download_test_data_path != "no" and FLAGS.data_dir):
    download_test_data(FLAGS.download_test_data_path,FLAGS.data_dir)

  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

  
=======
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
  if(FLAGS.zip_send_email=="yes"):
    zip_and_set_email(FLAGS.output_dir)
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107

