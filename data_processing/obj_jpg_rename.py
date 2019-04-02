import os
import datetime
import argparse

def get_path(data_dir):
    paths=[]
    classdict={}
    for root,_,files in os.walk(data_dir):
        classname=os.path.split(root)[1]
        if classname not in classdict.keys() and len(files)!=0:
            classdict[classname]=len(files)
        elif classname in classdict.keys() and len(files)!=0:
            classdict[classname] += len(files)
        for file in files:
            paths.append(os.path.join(root,file))
    return paths,classdict

def rename(oldname, newname):
    try:
        if oldname !='' and newname != '':
            os.rename(oldname, newname)
            print('old name:', oldname)
            print('new name:', newname)
    except Exception as ex:
        print(ex)

def renames(paths,classdict):
    cur_date = datetime.datetime.now()
    str_date = '{year}-{month}-{day}'.format(year=cur_date.year, month=cur_date.month, day=cur_date.day)
    for path in paths:
        dirname=os.path.split(path)[0]
        classname=os.path.split(dirname)[1]
        filename='{}_{}_{}.jpg'.format(classname,str_date,classdict[classname])
        classdict[classname] -=1
        rename(path,os.path.join(dirname,filename))

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='FUSION setting.')
    parser.add_argument('--jpg_path', dest='jpg_path',
                        help='path to jpg dir',
                        default='/home/hyl/data/data-lyl/obj_jpg_2018-12-28_600classes', type=str)#指定excel

    args = parser.parse_args()
    return args

if __name__=='__main__':
    args = parse_args()
    data_dir= args.jpg_path
    paths, classdict=get_path(data_dir)
    renames(paths, classdict)
