

#include "yolodet.h"
#include <numeric>

namespace Yolov5Det {
    
    YOLODET::YOLODET(){
    };

void YOLODET::DetInit(int deviceid, const string& engine_file, float confidence_threshold, float nms_threshold) {
    // auto engine = std::make_shared<Yolo::create_infer>(
    // 
    this->engine = Yolo::create_infer(
    engine_file,                // engine file
    Yolo::Type::V5,                       // yolo type, Yolo::Type::V5 / Yolo::Type::X
    deviceid,                   // gpu id
    confidence_threshold,                      // confidence threshold 0.25f
    nms_threshold,                      // nms threshold  0.45f
    Yolo::NMSMethod::FastGPU,   // NMS method, fast GPU / CPU
    1024,                       // max objects
    false                       // preprocess use multi stream
    );
    
    if(this->engine == nullptr){
        std::cout << "Engine is nullptr" << std::endl;
        //INFOE("Engine is nullptr");
        //return;
    }
};
    
void YOLODET::DetUnInit(){
    if(this->engine.get() != nullptr){
        this->engine.reset();
    }
    
};


ObjectDetector::BoxArray YOLODET::commit_gpu(cv::Mat srcimg){

    if(this->engine == nullptr){
        std::cout << "Engine is nullptr!!!" << std::endl;
        }
    // 推理并获取结果
    auto det_result = this->engine->commit(srcimg).get();  // 得到的是vector<Box>

    return det_result;
}; // namespace PaddleOCR


YOLODET::~YOLODET() {
  DetUnInit();
  //this->engine.reset();
  // if (this->engine != nullptr) {
  //   delete this->engine;
  // }
};

} // namespace PaddleOCR
