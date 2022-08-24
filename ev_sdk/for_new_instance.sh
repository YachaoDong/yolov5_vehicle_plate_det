# 用于重建实例，重新下载 cudnn tensorrt paddle_inference

# 1. cudnn
cd /project/train/src_repo
wget https://extremevision-js-userfile.oss-cn-hangzhou.aliyuncs.com/user-4467-files/0b9f2718-5c24-4a26-bc07-4b5f0e3305ef/cudnn-11.2-linux-x64-v8.1.1.33.tgz
tar -xvf cudnn-11.2-linux-x64-v8.1.1.33.tgz
cp cuda/include/*.h /usr/include/
cp cuda/lib64/libcudnn* /usr/lib/x86_64-linux-gnu/

# 2. tensorrt
wget https://extremevision-js-userfile.oss-cn-hangzhou.aliyuncs.com/user-4467-files/41bf036e-0f67-4cea-ae9e-00404d7e7e52/TensorRT-8.4.1.5.tar.gz
tar -xvf TensorRT-8.4.1.5.tar.gz
cp TensorRT-8.4.1.5/include/*.h /usr/include/x86_64-linux-gnu/
cp TensorRT-8.4.1.5/include/lib* /usr/lib/x86_64-linux-gnu/
# 删除原文件
rm cudnn-11.2-linux-x64-v8.1.1.33.tgz TensorRT-8.4.1.5.tar.gz
rm -rf cuda/ TensorRT-8.4.1.5/


# 3. paddle_inference
wget https://extremevision-js-userfile.oss-cn-hangzhou.aliyuncs.com/user-4467-files/93f199c7-5099-4950-b70c-cfe68efd9070/paddle_inference.tgz
tar -xvf paddle_inference.tgz
rm paddle_inference.tgz
mv paddle_inference/ /usr/local/ev_sdk/3rd/

# TODO 移动缺失库


