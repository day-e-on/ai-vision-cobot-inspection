# ai-vision-robot-inspection
협동로봇 프로젝트

````markdown
# AI Vision-Based Cobot Inspection System

WISET AI 로봇 시스템 엔지니어 전문인력 양성과정에서 수행한  
AI 비전 및 협동로봇 프로젝트를 정리한 저장소입니다.

CNN 이미지 분류부터 YOLO 객체 검출, ResNet 기반 이상 탐지까지 학습한 뒤,  
최종적으로 비전 인공지능과 두산 협동로봇을 연동하여  
양품과 불량품을 자동으로 분류하는 시스템을 구현했습니다.

---

## Project Overview

이 저장소는 다음 네 단계의 프로젝트로 구성되어 있습니다.

```text
01. CNN 기반 이미지 분류
02. YOLO 기반 객체 검출 및 위치 인식
03. ResNet 기반 Anomaly Detection
04. AI 비전과 협동로봇을 연동한 자동 분류 시스템
````

각 프로젝트에서 개발한 모델과 기능을 최종 협동로봇 시스템에 통합했습니다.

---

## System Workflow

```text
RealSense 카메라 촬영
        ↓
YOLO 기반 큐브 검출
        ↓
큐브 중심 좌표·깊이·회전각 계산
        ↓
ResNet 기반 이상 여부 판별
        ↓
카메라 좌표를 로봇 좌표로 변환
        ↓
두산 협동로봇 Pick & Place
        ↓
양품과 불량품을 서로 다른 위치로 분류
```

---

## Repository Structure

```text
ai-vision-cobot-inspection/
│
├── 01_cnn_classification/
│   └── CNN 기반 이미지 분류 실습
│
├── 02_yolo_segmentation/
│   └── YOLO를 활용한 큐브 검출 및 위치·회전각 추정
│
├── 03_resnet_anomaly_detection/
│   └── ResNet을 활용한 정상·이상 이미지 판별
│
├── 04_cobot_anomaly_sorting/
│   └── 비전 인공지능과 협동로봇을 연동한 자동 분류 시스템
│
├── assets/
│   └── 프로젝트 결과 이미지 및 시연 자료
│
└── README.md
```

---

## 01. CNN Classification

CNN의 기본 구조와 이미지 분류 과정을 이해하기 위해 수행한 프로젝트입니다.

* 이미지 데이터 전처리
* CNN 모델 구성
* 모델 학습 및 평가
* 새로운 이미지에 대한 추론

---

## 02. YOLO Segmentation

RealSense 카메라로 촬영한 영상에서 큐브를 검출하기 위해
YOLO Segmentation 모델을 학습하고 적용했습니다.

주요 기능은 다음과 같습니다.

* 큐브 객체 검출
* 객체별 마스크 추출
* 중심 픽셀 좌표 계산
* 깊이 정보 측정
* 큐브 회전각 추정

---

## 03. ResNet Anomaly Detection

정상 큐브 이미지를 학습한 ResNet 기반 모델을 활용하여
입력 이미지가 정상인지 이상인지 판별했습니다.

```text
Input Image
     ↓
YOLO 객체 영역 Crop
     ↓
ResNet Feature Extraction
     ↓
Anomaly Score 계산
     ↓
GOOD / NG 판정
```

설정한 임계값을 기준으로 Anomaly Score를 비교하여
양품과 불량품을 구분했습니다.

---

## 04. Cobot Anomaly Sorting

앞선 YOLO 및 ResNet 모델을 두산 협동로봇 M0609와 연동한
최종 AI 로봇 프로젝트입니다.

### 주요 기능

* RealSense D435 영상 입력
* YOLO 기반 큐브 위치 검출
* ResNet 기반 이상 탐지
* 카메라 좌표계에서 로봇 좌표계로 좌표 변환
* 큐브 위치와 회전각을 고려한 로봇 파지
* 판정 결과에 따른 양품·불량품 분리 적재
* 중앙 기어 조립 과정에서 순응제어 적용

---

## Tech Stack

### AI / Vision

* Python
* PyTorch
* Ultralytics YOLO
* CNN
* ResNet
* OpenCV
* NumPy

### Robot / Sensor

* Doosan Robotics M0609
* ROS 2
* RealSense D435
* Pick & Place
* Force Control
* Compliance Control

---

## Project Result

비전 센서로 작업물을 인식하고 AI 모델로 이상 여부를 판별한 뒤,
판정 결과에 따라 협동로봇이 작업물을 서로 다른 위치로 자동 분류하도록 구현했습니다.

이를 통해 다음 과정을 하나의 시스템으로 통합했습니다.

```text
Perception → AI Judgment → Coordinate Transformation
→ Robot Manipulation → Automatic Sorting
```

---

## Notes

모델 가중치와 전체 데이터셋은 파일 용량 및 데이터 관리 문제로
저장소에 포함하지 않았습니다.
