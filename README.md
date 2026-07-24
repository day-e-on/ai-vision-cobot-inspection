# ai-vision-robot-inspection
협동로봇 프로젝트

ai-vision-cobot-inspection/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── assets/
│   ├── images/
│   ├── results/
│   └── demo.gif
│
├── docs/
│   ├── system_architecture.png
│   ├── project_overview.md
│   └── troubleshooting.md
│
├── 01_cnn_classification/
│   ├── README.md
│   ├── train.py
│   ├── evaluate.py
│   ├── inference.py
│   ├── model.py
│   └── config.yaml
│
├── 02_yolo_segmentation/
│   ├── README.md
│   ├── train_yolo.py
│   ├── detect_cubes.py
│   ├── estimate_rotation.py
│   ├── dataset.yaml
│   └── config.yaml
│
├── 03_resnet_anomaly_detection/
│   ├── README.md
│   ├── train_anomaly.py
│   ├── anomaly_inference.py
│   ├── model.py
│   ├── preprocessing.py
│   └── config.yaml
│
├── 04_cobot_anomaly_sorting/
│   ├── README.md
│   ├── main.py
│   ├── robot.py
│   ├── camera.py
│   ├── vision_pipeline.py
│   ├── coordinate_transform.py
│   ├── pick_and_place.py
│   ├── anomaly_detector.py
│   └── config.py
│
└── shared/
    ├── __init__.py
    ├── visualization.py
    └── utils.py
