import os
from pathlib import Path
import glob
import random

def get_imgs_path(data_dir='/home/data/', save_dir_path='/home/data/labels/'):
    dirs = os.listdir(data_dir)
    abs_dirs = [os.path.join(data_dir, i) for i in dirs]
    det_dirs = []
    ocr_dirs = []
    for d in abs_dirs:
        files = os.listdir(d)
        
        ocr_flag = True
        for f in files:
            p = Path(f)
            if p.suffix == '.xml':
                det_files.append(d)
                ocr_flag = False
                break
        if ocr_flag:
            ocr_dirs.append[d]
    
    # 获得data目录下哪些是
    os.makedirs(save_dir_path, exist_ok='True')
    for d in det_dirs:
        for image_path in glob.glob(os.path.join(d + "*.jpg")):
            with open(save_dir_path + 'all_det.txt', 'w') as f1:
                for train_pwd in train_abs_img_paths:
                    f1.write(train_pwd + '\n')
    for d in ocr_dirs:
        for image_path in glob.glob(os.path.join(d + "*.jpg")):
            with open(save_dir_path + 'all_ocr.txt', 'w') as f1:
                for train_pwd in train_abs_img_paths:
                    f1.write(train_pwd + '\n')
    
    # 生成训练测试集，写入txt文件中
    with open(os.path.join(save_dir_path + 'all_det.txt')) as f1:
        all_det = f1.readlines()
        random.shuffle(all_det)
        
        num_imgs = len(all_det)
        train_percent = 0.9
        train_abs_img_paths = all_det[:int(train_percent*num_imgs)]
        test_abs_img_paths = all_det[int(train_percent*num_imgs):]
    
        with open(os.path.join(save_dir_path + 'train.txt'), 'w') as f1:
            for train_pwd in train_abs_img_paths:
                f1.write(train_pwd)

        with open(os.path.join(save_dir_path + 'test.txt'), 'w') as f1:
            for test_pwd in test_abs_img_paths:
                f1.write(test_pwd)

        with open(os.path.join(save_dir_path + 'val.txt'), 'w') as f1:
            for val_pwd in test_abs_img_paths:
                f1.write(val_pwd)

    
            

            
                
            
                
                
        