#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/dnn.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/videoio.hpp>



struct Detection
{
    int class_id{0};
    std::string className{};
    float confidence{0.0};
    cv::Scalar color{};
    cv::Rect box{};
};

cv::Mat formatToSquare(const cv::Mat &source)
{
    int col = source.cols;
    int row = source.rows;
    int _max = MAX(col, row);
    cv::Mat result = cv::Mat::zeros(_max, _max, CV_8UC3);
    source.copyTo(result(cv::Rect(0, 0, col, row)));
    return result;
}

int main() {

    float modelConfidenseThreshold {0.25};
    float modelScoreThreshold      {0.45};
    float modelNMSThreshold        {0.50};



    cv::dnn::Net net = cv::dnn::readNetFromONNX("best.onnx");

    cv::VideoCapture cap;
    cap.open(0);

    if (!cap.isOpened()) {
        std::cout << " Ошибка открытия камеры." << std::endl;
        return -1;
    }

    cv::Mat image;
    while (true) {
        cap >> image;
        if (image.empty()) {
            break;
        }


//    auto image = cv::imread("D:\\clionProject\\Ilya\\img.png");
//    cv::resize(image, image, cv::Size(image.cols / 2, image.rows / 2));

    cv::Mat modelInput = image;
//    modelInput = formatToSquare(modelInput);

    float dw = 0;
    float dh = 0;

    cv::Size shape(image.cols, image.rows);

    cv::Size newShape(640, 640);

    float r = std::min((float) newShape.width / (float) shape.width, (float) newShape.height / (float) shape.height);

    cv::Point2f ration(r, r);
    cv::Size newUnpad((int)std::round(shape.width * ration.x), (int)std::round(shape.height * ration.y));

    dw = newShape.width - newUnpad.width;
    dh = newShape.height - newUnpad.height;

    auto realsize = newUnpad;

    dw /= 2;
    dh /= 2;

    cv::resize(modelInput, modelInput, newUnpad, cv::INTER_LINEAR);

    int top = (int)(std::round(dh - 0.1));
    int bot = (int)(std::round(dh + 0.1));

    int left = (int)(std::round(dw - 0.1));
    int right = (int)(std::round(dw + 0.1));

    float _offsetX = (float) dw;
    float _offsetY = (float) dh;

    std::cout << _offsetX << " " << _offsetY << std::endl;

    cv::copyMakeBorder(modelInput, modelInput, top, bot, left, right, cv::BORDER_CONSTANT, cv::Scalar(114, 114, 114));
    cv::Mat blob = cv::dnn::blobFromImage(modelInput, 1/255.0, cv::Size(640, 640), cv::Scalar(), true, false);

    net.setInput(blob);

    std::vector<cv::Mat> outputs;
    net.forward(outputs, net.getUnconnectedOutLayersNames());

    int rows = outputs[0].size[1];
    int dimensions = outputs[0].size[2];

    bool yolov8 = false;

    if (dimensions > rows) // Check if the shape[2] is more than shape[1] (yolov8)
    {
        yolov8 = true;
        rows = outputs[0].size[2];
        dimensions = outputs[0].size[1];

        outputs[0] = outputs[0].reshape(1, dimensions);
        cv::transpose(outputs[0], outputs[0]);
    }

    float *data = (float *)outputs[0].data;

    float x_factor = image.cols / realsize.width;
    float y_factor = image.rows / realsize.height;

    _offsetY = _offsetY * x_factor;
    _offsetX = _offsetX *x_factor;


    std::vector<int> class_ids;
    std::vector<float> confidences;
    std::vector<cv::Rect> boxes;

    for (int i = 0; i < rows; ++i) {
        float *classes_scores = data+4;

        cv::Mat scores(1, 1, CV_32FC1, classes_scores);
        cv::Point class_id;
        double maxClassScore;
        cv::minMaxLoc(scores, 0, &maxClassScore, 0, &class_id);

        if (maxClassScore > modelScoreThreshold) {
            confidences.push_back(maxClassScore);
            class_ids.push_back(class_id.x);

            float x = data[0];
            float y = data[1];
            float w = data[2];
            float h = data[3];

            int left = int(x / ration.x - dw / ration.x);
            int top = int(y / ration.y - dh / ration.y);

            int right = int((x + 0.5 * w) * x_factor);
            int bot = int((y + 0.5 * h) * y_factor);
            int width = int(w / ration.x);
            int height = int(h / ration.y);

            boxes.push_back(cv::Rect(left, top, width, height));
        }
        data+=dimensions;
    }

    std::vector<int> nms_results;
    cv::dnn::NMSBoxes(boxes, confidences, modelScoreThreshold, modelNMSThreshold, nms_results);

    for (unsigned long i = 0; i < nms_results.size(); ++i) {
        int idx = nms_results[i];

        Detection result;
        result.class_id = class_ids[idx];
        result.confidence = confidences[idx];

        result.box = boxes[idx];
        auto box = result.box;
        cv::rectangle(image, cv::Point(box.x - box.width/2, box.y - box.height / 2), cv::Point(box.x + box.width / 2, box.y + box.height / 2),
                      cv::Scalar(0, 255, 0), 2);

    }

    cv::imshow("Image", image);
    cv::waitKey(5);
    }

    cv::destroyAllWindows();

    return 0;
}


