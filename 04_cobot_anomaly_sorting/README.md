## Model Preparation

동작 영상 : https://mysterious-broccoli-188.notion.site/AI-3a7af7312d1d80c0aa91dc4cb98e3fdb?source=copy_link

최종 로봇 시스템에 사용한 이상 탐지 모델은 다음 과정으로 준비했습니다.

1. YOLO Segmentation 모델로 작업 영역의 큐브를 검출
2. RealSense 카메라를 이용해 정상 큐브 이미지 수집
3. YOLO 마스크 또는 Bounding Box를 기준으로 객체 영역 Crop
4. Crop 이미지를 입력 데이터로 사용해 ResNet 기반 이상 탐지 모델 학습
5. 학습된 모델을 최종 협동로봇 분류 시스템에 연동

관련 코드는 다음 폴더에서 확인할 수 있습니다.

- YOLO 검출: `../02_yolo_segmentation`
- 데이터 전처리 및 ResNet 학습: `../03_resnet_anomaly_detection`
