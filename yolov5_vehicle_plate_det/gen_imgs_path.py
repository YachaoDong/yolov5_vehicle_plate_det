import os
from pathlib import Path

def get_imgs_path(data_dir='/home/data/'):
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
    
    for d in det_dirs:
        
    
return det_dirs, ocr_dirs
            
                
            
                
                
        