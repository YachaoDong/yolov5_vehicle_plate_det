#run.sh

# 如果存在要保存的文件，提前删除文件夹
# rm  -r /home/data/vehicle_data/*

 

#创建数据集相关文件夹
mkdir  -p /project/.config/Ultralytics/
mkdir  -p /home/data/vehicle_data/labels

# 生成all imgs abs path txt
ls /home/data/1*/.jpg > /home/data/vehicle_data/all_det.txt



# sheng

# 生成img 绝对路径 txt
python /project/train/src_repo/yolov5_vehicle_plate_det/gen_imgs_path.py



# xml转txt labels
python /project/train/src_repo/yolov5_vehicle_plate_det/xml2labels.py



#执行YOLOV5训练脚本
# pip install -r /project/train/src_repo/yolov5_vehicle_plate_det/requirements.txt

cp /project/train/src_repo/yolov5_vehicle_plate_det/Arial.ttf  /project/.config/Ultralytics/

python /project/train/src_repo/yolov5_vehicle_plate_det/train.py   --batch-size 32 --weights /project/train/src_repo/yolov5_vehicle_plate_det/yolov5s.pt  --epochs 100 --workers 4

python /project/train/src_repo/yolov5_vehicle_plate_det/train.py   --batch-size 16 --weights /project/train/src_repo/yolov5_vehicle_plate_det/yolov5s.pt  --epochs 100 --workers 4



