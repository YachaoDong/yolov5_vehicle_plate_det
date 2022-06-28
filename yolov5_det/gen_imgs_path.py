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

def gen_imgs_path():
    
    
    # 生成训练测试集，写入txt文件中
    with open('/home/data/vehicle_data/all_det_imgs.txt', 'r') as f1:
        all_det = f1.readlines()
        random.shuffle(all_det)
        
        num_imgs = len(all_det)
        train_percent = 0.9
        train_abs_img_paths = all_det[:int(train_percent*num_imgs)]
        test_abs_img_paths = all_det[int(train_percent*num_imgs):]
    
        with open('/home/data/vehicle_data/train.txt', 'w') as f1:
            for train_pwd in train_abs_img_paths:
                f1.write(train_pwd)

        with open('/home/data/vehicle_data/test.txt', 'w') as f1:
            for test_pwd in test_abs_img_paths:
                f1.write(test_pwd)

        with open('/home/data/vehicle_data/val.txt', 'w') as f1:
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
    
        


            
                
            
                
                
        