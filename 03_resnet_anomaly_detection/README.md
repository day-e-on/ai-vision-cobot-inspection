# Wide-ResNet50 Anomaly Detection

This directory contains the anomaly detection module used to inspect cube objects.

The model is trained only on normal cube images and detects anomalous samples by comparing features extracted from a pretrained Wide-ResNet50-2 encoder with features reconstructed by a decoder.

The trained model is later integrated with the YOLO-based cube detection and collaborative robot sorting pipeline.

---

## Overview

The anomaly detection pipeline consists of the following steps:

```text
RealSense image collection
        ↓
Normal cube dataset construction
        ↓
Wide-ResNet50 feature extraction
        ↓
Feature reconstruction through bottleneck and decoder
        ↓
Encoder-decoder feature comparison
        ↓
Anomaly map and anomaly score generation
        ↓
GOOD / BAD classification
```

Unlike conventional supervised classification, the model is trained using only normal samples. Therefore, it can detect previously unseen defects without requiring every defect type during training.

---

## Model Architecture

This implementation follows a Reverse Distillation-based anomaly detection structure.

```text
Input Image
    ↓
Pretrained Wide-ResNet50-2 Encoder
    ↓
Multi-scale Feature Maps
    ↓
Bottleneck Layer
    ↓
Decoder
    ↓
Reconstructed Feature Maps
    ↓
Cosine Distance
    ↓
Anomaly Map
```

### Encoder

The encoder uses an ImageNet-pretrained Wide-ResNet50-2 model.

It extracts multi-scale features from the input image. The encoder remains frozen during training and is used as the reference network for normal feature representations.

### Bottleneck

The bottleneck combines the multi-scale encoder features and converts them into a representation that can be processed by the decoder.

### Decoder

The decoder reconstructs the original encoder features from the bottleneck output.

For normal images, the reconstructed features are expected to be similar to the encoder features. Defective regions produce larger feature differences.

### Anomaly Score

The anomaly map is calculated using cosine distance:

```text
Anomaly value = 1 - cosine similarity
```

A lower score indicates that the image is similar to the learned normal pattern, while a higher score indicates a greater possibility of an anomaly.

---

## Directory Structure

```text
03_resnet_anomaly_detection/
├── RD_Trainer.ipynb
├── RD_Tester.ipynb
├── realsense2.ipynb
├── resnet.py
├── de_resnet.py
├── dataset.py
├── README.md
│
├── data/
│   └── cube/
│       ├── train/
│       │   └── good/
│       └── test/
│           ├── good/
│           └── anomaly/
│
├── checkpoints/
│   └── wres50_cube.pth
│
└── visualization/
    └── cube/
```

> `dataset.py` is required because both training and testing notebooks import `get_data_transforms` and `RD_Dataset`.

---

## File Description

| File | Description |
|---|---|
| `realsense2.ipynb` | Collects cube images using an Intel RealSense camera |
| `RD_Trainer.ipynb` | Trains the anomaly detection model using normal cube images |
| `RD_Tester.ipynb` | Calculates anomaly scores, visualizes anomalous regions, and evaluates thresholds |
| `resnet.py` | Defines the Wide-ResNet50-2 encoder and bottleneck |
| `de_resnet.py` | Defines the decoder used to reconstruct encoder features |
| `dataset.py` | Defines image transformations and the anomaly detection dataset |
| `wres50_cube.pth` | Stores the trained bottleneck and decoder weights |

---

## Dataset Structure

The training set contains only normal cube images.

```text
data/
└── cube/
    ├── train/
    │   └── good/
    │       ├── 000.png
    │       ├── 001.png
    │       └── ...
    │
    └── test/
        ├── good/
        │   ├── 000.png
        │   └── ...
        │
        └── anomaly/
            ├── 000.png
            └── ...
```

- `train/good`: normal images used for model training
- `test/good`: normal images used for evaluation
- `test/anomaly`: defective images used for evaluation

---

## Data Collection

Run `realsense2.ipynb` to collect images using the Intel RealSense camera.

### Camera Configuration

| Parameter | Value |
|---|---:|
| Resolution | 1280 × 720 |
| Frame rate | 30 FPS |
| Saved crop size | 512 × 512 |

The notebook displays a centered square crop of the camera frame.

### Keyboard Controls

| Key | Action |
|---|---|
| `s` | Save the current cropped image |
| `q` | Stop image collection |

The save directory can be changed depending on the type of data being collected.

```python
save_category = "./data/cube/train/good"
```

Other examples:

```python
save_category = "./data/cube/test/good"
save_category = "./data/cube/test/anomaly"
```

Images are saved sequentially as:

```text
000.png
001.png
002.png
...
```

---

## Training

Open and run:

```text
RD_Trainer.ipynb
```

### Training Configuration

| Parameter | Value |
|---|---:|
| Model | Wide-ResNet50-2 |
| Epochs | 50 |
| Batch size | 16 |
| Learning rate | 0.005 |
| Input image size | 256 × 256 |
| Optimizer | Adam |
| Adam betas | `(0.5, 0.999)` |
| Random seed | 111 |

The encoder is loaded with pretrained ImageNet weights and remains frozen during training.

Only the bottleneck and decoder are optimized.

```python
encoder.eval()

optimizer = torch.optim.Adam(
    list(decoder.parameters()) + list(bn.parameters()),
    lr=learning_rate,
    betas=(0.5, 0.999)
)
```

The training loss is calculated from the cosine distance between the encoder features and reconstructed decoder features.

```python
loss += torch.mean(
    1 - cosine_similarity(
        encoder_feature,
        decoder_feature
    )
)
```

---

## Model Checkpoint

The model is saved every 10 epochs.

```text
checkpoints/wres50_cube.pth
```

The checkpoint contains:

```python
{
    "bn": bn.state_dict(),
    "decoder": decoder.state_dict()
}
```

The pretrained encoder weights are not stored in this checkpoint. They are loaded separately when the model is used.

---

## Evaluation

Open and run:

```text
RD_Tester.ipynb
```

The notebook provides three main evaluation functions.

### Anomaly Visualization

```python
visualization(
    "cube",
    "./visualization/cube/"
)
```

This function generates anomaly heatmaps by comparing the encoder and decoder feature maps.

A Gaussian filter is applied to reduce noise in the anomaly map.

```python
anomaly_map = gaussian_filter(
    anomaly_map,
    sigma=4
)
```

### Anomaly Score Calculation

```python
img_labels, anomaly_scores = anomaly_score_calculator("cube")
```

The maximum value of the anomaly map is used as the image-level anomaly score.

```python
image_score = np.max(anomaly_map)
```

The test scores are then normalized between 0 and 1 using min-max normalization.

A higher normalized score indicates a greater possibility of a defect.

### Threshold Search

```python
best_threshold("cube")
```

The threshold is evaluated from `0.001` to `1.000` in increments of `0.001`.

The notebook reports:

- Accuracy
- Precision
- Recall
- F1-score
- False positives
- False negatives

A specific threshold can also be evaluated manually.

```python
classification_with_threshold(
    "cube",
    threshold=0.3
)
```

The threshold value should be selected based on the score distributions of normal and defective test samples.

---

## Execution Order

### 1. Collect Images

```bash
jupyter notebook realsense2.ipynb
```

Collect normal training images and normal/defective test images.

### 2. Train the Model

```bash
jupyter notebook RD_Trainer.ipynb
```

After training, the following checkpoint is generated:

```text
checkpoints/wres50_cube.pth
```

### 3. Evaluate the Model

```bash
jupyter notebook RD_Tester.ipynb
```

Use the notebook to visualize defective regions and determine a suitable classification threshold.

---

## Requirements

```text
Python
PyTorch
torchvision
NumPy
OpenCV
Matplotlib
SciPy
scikit-learn
scikit-image
pandas
Pillow
natsort
pyrealsense2
Jupyter Notebook
```

Example installation:

```bash
pip install torch torchvision
pip install numpy opencv-python matplotlib scipy
pip install scikit-learn scikit-image pandas
pip install pillow natsort pyrealsense2 jupyter
```

---

## Integration with the Robot System

The trained anomaly detection model is used in the final robot inspection pipeline.

```text
RealSense Camera
        ↓
YOLO Cube Detection
        ↓
Detected Cube Crop
        ↓
Wide-ResNet50 Anomaly Detection
        ↓
GOOD / BAD Decision
        ↓
Collaborative Robot Sorting
```

YOLO detects the position and orientation of each cube. The detected cube region is cropped and passed to the anomaly detection model.

The collaborative robot then places normal and defective cubes in different locations according to the inspection result.

---

## Notes

### Keep Training and Inference Preprocessing Consistent

The following conditions should remain as similar as possible between training and inference:

- Crop area
- Object size within the image
- Input resolution
- Camera position
- Object orientation
- Lighting condition
- Background
- Image normalization

Differences in preprocessing may cause normal cubes to receive high anomaly scores.

### Threshold Calibration

The anomaly score is not a probability.

The evaluation notebook uses min-max normalized test scores, while a real-time inference script may use raw anomaly scores. Therefore, thresholds obtained from different score calculation methods are not directly interchangeable.

The final threshold should be calibrated using normal and defective samples collected in the actual operating environment.

### Model Weight File

The `.pth` checkpoint may be too large for a standard GitHub commit.

Consider using one of the following:

- Git LFS
- GitHub Releases
- External cloud storage

---

## Result

The trained model detects defective cube regions by measuring the difference between learned normal features and reconstructed features.

The model output is used by the collaborative robot system to automatically separate normal and defective products.
