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

def gen_imgs_path(data_dir='/home/data/', save_dir_path='/home/data/vehicle_data/labels/'):
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
                det_files.append(d)
                ocr_flag = False
                break
        if ocr_flag:
            ocr_dirs.append[d]
    
    # 将det 和 ocr 的 img 绝对路径写入txt中
    os.makedirs(save_dir_path, exist_ok='True')
    for d in det_dirs:
        for image_path in glob.glob(os.path.join(d, "*.jpg")):
            for train_pwd in image_path:
                with open(save_dir_path + 'all_det.txt', 'w') as f1:
                    f1.write(train_pwd + '\n')
                
                with open(save_dir_path + 'all_det_xmls.txt', 'w') as f2:
                    f2.write(train_pwd.replace('.jpg', '.xml') + '\n')
                    
    for d in ocr_dirs:
        for image_path in glob.glob(os.path.join(d, "*.jpg")):
            with open(save_dir_path + 'all_ocr.txt', 'w') as f1:
                for train_pwd in image_path:
                    f1.write(train_pwd + '\n')
    
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
    
    return det_dirs, ocr_dirs


# 将xml转换为yolov5labels
# box: [0,6], line:[6], key_point:[7, 14]
classes = ['truck', 'van', 'car', 'slagcar', 'bus', 'fire_truck',
           'police_car', 'ambulance',  'SUV', 'microbus', 'unknown_vehicle',
           'plate', 'double_plate']

vehicle_color = ['white', 'silver', 'grey', 'black', 'red', 'blue', 'yellow', 'green', 'brown', 'others']

abs_path = os.getcwd()

def convert_annotation(xml_path,
                       txt_dir_path='/project/train/src_repo/dataset/labels/'):
    in_file = open(xml_path, encoding='utf-8')
    xml_p = Path(xml_path)
    out_file = open(txt_dir_path + xml_p.stem + '.txt', 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    def convert(size, box):
        # box: xmin, xmax, ymin, ymax
        dw = 1. / (size[0])
        dh = 1. / (size[1])
        x = (box[0] + box[1]) / 2.0 - 1
        y = (box[2] + box[3]) / 2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)
    
    # car bbox obj
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        # 获取类别
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)

        # 获取bbox
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        # bbox转换 xyxy 转换为 xywh(0~1)
        # bb = convert((w, h), b)
        bb = (b[0]/w, b[2]/h, b[1]/w, b[3]/h)

        # 获取颜色
        color = obj.find('attributes').find('attribute').find('value').text
        if color not in vehicle_color:
            continue
        color_id = vehicle_color.index(color)

        # 写入 cls_id + color_id + bbox
        out_file.write(str(cls_id) + " " + str(color_id) + " " + " ".join([str(a) for a in bb]))
        # 换行
        out_file.write('\n')

    # plate poly obj
    for obj in root.iter('polygon'):
        # difficult = obj.find('difficult').text

        # 获取类别
        cls = obj.find('class').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)

        # 获取颜色
        color = ' '
        for attribute in obj.find('attributes').iter('attribute'):
            if attribute.find('name').text == 'color':
                color = attribute.find('value').text

        if color not in vehicle_color:
            continue
        color_id = vehicle_color.index(color)

        # 获取bbox
        points = obj.find('points').text
        points = points.split(';')   # ["x1,y1", "x2,y3", "x3,y3","x4,y4"]
        poly = []
        for i in points:
            x = float(i.split(',')[0]) / w
            y = float(i.split(',')[1]) / h
            poly.append(x)
            poly.append(y)

        # 写入 cls_id + color_id + poly
        out_file.write(str(cls_id) + " " + str(color_id) + " " + " ".join([str(a) for a in poly]))
        # 换行
        out_file.write('\n')
    
    
    


if __name__ == '__main__':
    # 设置参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/home/data/', help='input img label path')
    parser.add_argument('--save_dir_path', type=str, default='/home/data/vehicle_data/labels/', help='input img label path')
    
    opt = parser.parse_args()
    
    # labels文件夹中生成  all_det.txt  all_ocr.txt  all_det_xmls.txt  train.txt  test.txt  val.txt
    gen_imgs_path(opt.data_dir, opt.save_dir_path)


            
                
            
                
                
        