import os
from pathlib import Path
import glob
import random
import xml.etree.ElementTree as ET
import pickle
from os import listdir, getcwd
from os.path import join
import argparse
import glob
import shutil

def gen_imgs_path(data_dir='/home/data/', save_dir_path='/home/data/vehicle_data/', save_img_path='/home/data/vehicle_data/images/'):
    dirs = os.listdir(data_dir)
    abs_dirs = [os.path.join(data_dir, i) for i in dirs]
    det_dirs = []
    ocr_dirs = []
    
    # 获得data目录下哪些是检测数据集的目录，哪些是ocr数据集目录
    for d in abs_dirs:
        files = os.listdir(d)
        
        ocr_flag = True
        for f in files:
            p = Path(f)
            if p.suffix == '.xml':
                det_dirs.append(d)
                ocr_flag = False
                break
        if ocr_flag:
            ocr_dirs.append(d)
    
    # 将det 和 ocr 的 img 绝对路径写入txt中
    # os.makedirs(save_dir_path, exist_ok='True')
    
    for d in det_dirs:
        with open(save_dir_path + 'all_det.txt', 'w') as f1:
            for image_path in glob.glob(os.path.join(d, "*.jpg")):
                image_name = image_path.split(os.sep)[-1].split('.')[0]
                f1.write(join(save_img_path, (image_name + '.jpg')) + '\n')

        with open(save_dir_path + 'all_det_xmls.txt', 'a') as f2:
            for image_path in glob.glob(os.path.join(d, "*.jpg")):
                f2.write(image_path.replace('.jpg', '.xml') + '\n')
        
        
                    
    
    for d in ocr_dirs:
        for image_path in glob.glob(os.path.join(d, "*.jpg")):
            with open(save_dir_path + 'all_ocr.txt', 'a') as f1:
                f1.write(image_path + '\n')
    
    
    # 生成训练测试集，写入txt文件中
    with open(os.path.join(save_dir_path, 'all_det.txt')) as f1:
        all_det = f1.readlines()
        random.shuffle(all_det)
        
        num_imgs = len(all_det)
        train_percent = 0.9
        train_abs_img_paths = all_det[:int(train_percent*num_imgs)]
        test_abs_img_paths = all_det[int(train_percent*num_imgs):]
    
        with open(os.path.join(save_dir_path, 'train.txt'), 'w') as f1:
            for train_pwd in train_abs_img_paths:
                f1.write(train_pwd)

        with open(os.path.join(save_dir_path, 'test.txt'), 'w') as f1:
            for test_pwd in test_abs_img_paths:
                f1.write(test_pwd)

        with open(os.path.join(save_dir_path, 'val.txt'), 'w') as f1:
            for val_pwd in test_abs_img_paths:
                f1.write(val_pwd)
    
    # return det_dirs, ocr_dirs



    
    


if __name__ == '__main__':
    # 设置参数
    # 生成img xml 路径参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/home/data/', help='input img label path')
    parser.add_argument('--save_dir_path', type=str, default='/home/data/vehicle_data/', help='input img label path')
    
    
    
    opt = parser.parse_args()
    
    # labels文件夹中生成  all_det.txt  all_ocr.txt  all_det_xmls.txt  train.txt  test.txt  val.txt
    gen_imgs_path(opt.data_dir, opt.save_dir_path)
    
        


            
                
            
                
                
        