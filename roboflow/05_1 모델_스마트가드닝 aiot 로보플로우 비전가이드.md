# 🌱 Smart Gardening AIoT — Roboflow Vision Guide (Overview)

이 문서는 스마트 가드닝 프로젝트에서 **Roboflow**를 어떻게 사용할지 전체 구조를 안내하는 개요 문서입니다.
센서 기반 제어 + 비전 기반 AI 진단을 결합한 형태의 시스템을 목표로 합니다.

---

## 📌 프로젝트 목표

식물 상태를 **센서 데이터 + 카메라 비전 분석**으로 판단하여

* 물 주기 자동 제어
* 빛/팬/환기/가습 자동 조절
* 병충해 조기 감지
* 성장 모니터링
  을 수행하는 **완전 자동 스마트 가드닝 시스템**을 구축한다.

Roboflow는 여기서 **비주얼 분석(컴퓨터 비전)** 전담 모듈 역할을 한다.

---

## 🧠 Roboflow를 쓰는 영역 (4대 모델)

### 1) 잎 건강 상태 분석 모델 (Leaf Health Detection)

* 잎의 **반점·변색·노화·말림·갈변** 등 비정상 패턴 감지
* 영양 부족, 과다비료, 빛 부족 등 초기 증상 인식
* **Classification** 또는 **Object Detection**

### 2) 토양 표면 상태 감지 모델 (Soil Surface Condition)

* 토양 **건조 / 과습 / 곰팡이 / 변색 / 이끼** 감지
* 센서 값과 함께 사용하면 정확도 대폭 상승
* **Classification** 또는 **Segmentation**

### 3) 해충 감지 모델 (Pest Detection)

* 응애·깍지벌레·진딧물·이물질 탐지
* 미세 객체여서 YOLO 기반 detection 권장
* **Object Detection**

### 4) 성장 측정 모델 (Growth Tracking / Segmentation)

* 잎 크기, 수, 줄기 길이 등 자동 측정
* 타임랩스 기반 성장 추적
* **Instance Segmentation**

---

## 📂 Roboflow 프로젝트 구조 권장 예시

```
/roboflow/
    /leaf-health/
        dataset/
        classes.txt
        export/
        model/
    /soil-condition/
        dataset/
        classes.txt
        model/
    /pest-detection/
        dataset/
        classes.txt
        model/
    /growth-tracking/
        dataset/
        masks/
        model/
```

---

## 🏗️ 스마트 가드닝 전체 파이프라인 (센서 + 비전 결합)

### 1) 센서 수집

* SHT31 (온습도)
* BH1750 (조도)
* 토양 습도 센서
* CO₂(optional)

### 2) 카메라 캡처

* Raspberry Pi 카메라
* ESP32-CAM
* USB Webcam

### 3) 비전 분석 (Roboflow Inference)

* 촬영된 이미지 → Roboflow model → json 결과
* 주요 필드:

```
healthy_leaf: true/false
soil_status: dry/wet/mold/normal
pest_detected: true/false
leaf_area: numeric
stem_length: numeric
```

### 4) 제어 로직 (IoT)

* 토양 건조 + 잎 정상 → 물 공급
* 잎 변색 + 조도 부족 → LED 증가
* 곰팡이 발생 → 팬/환기 작동
* 해충 감지 → 사용자 경고
* 성장 변화 기록 → 앱 대시보드 반영

---

## ⚡ Roboflow 모델 추천 아키텍처

* **YOLO11n / YOLOv8n** (가벼운 모델, Edge에서 고성능)
* **SAM(Segment Anything)** 기반 segmentation 가능
* 학습은 Roboflow Train 사용
* 배포는 Roboflow Inference Server 또는 로컬 Docker 권장

---

## 📈 데이터 구축 가이드 요약

### 최소 확보해야 하는 데이터

| 모델    | 필요 이미지 수 | 주 라벨                           |
| ----- | -------- | ------------------------------ |
| 잎 진단  | 200~500  | normal, yellow, brown, spotted |
| 토양    | 150~300  | dry, wet, mold, moss           |
| 해충    | 100+     | pest, none                     |
| 성장 측정 | 100+     | plant mask                     |

### 필수 전처리

* 다양한 조명 (낮/밤/LED)
* 다양한 거리·각도
* augmentation 적극 사용 (Roboflow 자동 제공)

---

## 🧩 Edge Device 구성

* Raspberry Pi:

```
pip install inference
inference server start
```

* ESP32-CAM:

  * 저해상도 → 서버 전송 방식 권장
  * 로컬 inference는 라즈베리파이에서 처리

---

## 📡 API 예시

```python
from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="http://localhost:9001",
    api_key="YOUR_KEY"
)

with client.use_model("leaf-health-model/1"):
    result = client.infer("plant.jpg")
    print(result)
```

---

## 🎯 MVP 우선순위

1. **토양 상태 감지** (가장 체감 큰 기능)
2. **잎 건강 진단**
3. 해충 감지
4. 성장 측정(부가 기능)

---

## ✔️ 결론

스마트 가드닝 프로젝트에서 Roboflow는 센서가 할 수 없는 **시각 기반 판단 시스템** 전체를 담당한다.
최종적으로 4가지 모델이 모두 필요하지만, 개발 순서는 **토양 → 잎 → 해충 → 성장** 순이 가장 현실적이다.

---

📄 다음 파일: **06_Python_추론_서버_가이드라인.md**

