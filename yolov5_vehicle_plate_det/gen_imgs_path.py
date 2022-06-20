import os
from pathlib import Path
import glob

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
                    
    with open(save_dir_path + 'all_det.txt') as f1:
        for img_path in f.read().strip
    
            

            
                
            
                
                
        