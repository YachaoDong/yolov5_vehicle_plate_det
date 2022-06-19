import os
from pathlib import Path

def get_imgs_path(data_dir='/home/data/'):
    dirs = os.listdir(data_dir)
    abs_dirs = [os.path.join(data_dir, i) for i in dirs]
    for d in abs_dirs:
        files = os.listdir(d)
        for f in files:
            p = Path(f)
            if p.suffix == ''
        