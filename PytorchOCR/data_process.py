# -*- coding: utf-8 -*-
'''
@Time    : 6/27/2022 4:23 PM
@Author  : dong.yachao
'''
import os
from os.path import join
import glob


# 将文件名为ocr内容的jpg文件转换为 text line数据集格式
def get_text_line(img_path_dir):
    img_names = glob.glob(join(img_path_dir, '*.jpg'))
    # print(img_names)

    # 写入Text Line 格式
    with open('ocr_data.txt', 'w', encoding='utf-8') as f1:
        for img_name in img_names:
            f1.write(img_name)
            f1.write('\t')
            content = os.path.basename(img_name).split('_')[0]
            f1.write(content)
            f1.write('\n')


# 生成车牌字典txt
def gen_alphabets():
    plateDict = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘",
                 "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学",
                 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                 'V', 'W',
                 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '~'
                 ]
    with open('alphabets.txt', 'w', encoding='utf-8') as f1:

        for val in plateDict:
            f1.write(val)
            f1.write('\n')

if __name__ == '__main__':
    img_path_dir = r'D:\CodeFiles\data\vehicle_data\car_plate'
    # get_text_line(img_path_dir)
    gen_alphabets()

