#run.sh

# 如果存在要保存的文件，提前删除文件夹
rm  -r /home/data/vehicle_data/*


#创建数据集相关文件夹
# mkdir  -p /home/data/vehicle_data/images
mkdir  -p /home/data/vehicle_data/labels
mkdir  -p /home/data/vehicle_data/xmls


# 拷贝图像
# cp /home/data/*/*.jpg  /home/data/smoke_data/images/
# 拷贝xml
cp /home/data/*/*.xml  /home/data/smoke_data/xmls/

# xml转txt labels
python /project/train/src_repo/yolov5_smoke/xml2labels.py

#数据集划分、转换, 生成训练测试 txt文件
python /project/train/src_repo/yolov5_smoke/split_train_val.py

#执行YOLOV5训练脚本
python /project/train/src_repo/yolov5_smoke/train.py   --batch-size 16 --weights /project/train/models/exp2/weights/last.pt --noplots

python /project/train/src_repo/yolov5_smoke/train.py   --batch-size 8 --weights /project/train/models/exp2/weights/last.pt --noplots


