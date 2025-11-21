# 🐛 Pest Detection Model Guide

스마트 가드닝 프로젝트 — 해충 감지 모델

이 문서는 식물 주변에서 발생하는 **해충(벌레)** 을 자동 감지하기 위한
Roboflow 기반 Object Detection 모델 구축 가이드이다.

---

## 📌 모델 목표

카메라로 촬영한 식물 이미지에서 다음과 같은 해충을 자동 탐지한다:

* **aphid (진딧물)**
* **mite (응애)**
* **scale insect (깍지벌레)**
* **larva/egg (유충/알)**
* **unknown pest (미정 벌레)**

특징:

* 크기가 매우 작음 → **Detection 모델 필수**
* 환경 따라 잘 안 보일 수 있음 → 고해상도 권장

---

## 🧩 Detection 모델이 필요한 이유

해충은 **한 이미지 안에 여러 개** 존재할 수 있고
위치·크기를 파악해야 하므로 **Classification은 부적합**.

따라서 YOLO 기반 Object Detection이 가장 적합하다.

---

## 📁 Dataset 구조

```
classes:
  - aphid
  - mite
  - scale
  - egg
  - pest
```

### 최소 권장 이미지 수

| 클래스          | 권장 데이터 |
| ------------ | ------ |
| aphid        | 40~60  |
| mite         | 40~60  |
| scale        | 20~40  |
| egg          | 20~40  |
| unknown pest | 20~40  |

총 150~250장으로 1차 MVP 가능.

---

## 📸 데이터 수집 팁

### 1) 가까이 촬영해야 함

* 5~10cm 거리
* 고해상도 (1080p 이상 권장)

### 2) 다양한 배경

* 잎 위
* 줄기 위
* 토양 표면
* 화분 벽

### 3) 벌레가 없을 때도 촬영

* negative samples 포함
* false-positive 방지

---

## 🔖 Annotation 방식

* **Bounding Box (필수)**
* 작은 객체이므로 박스는 정밀하게 잡아야 함
* Roboflow의 AI-assisted 기능(autodistill) 활용 추천

---

## 🧪 학습 설정 추천

* **Model:** YOLO11n / YOLOv8n
* **Image Size:** 640
* **Augmentations:**

  * Mosaic (벌레가 작아서 효과 좋음)
  * Flip horizontal
  * Exposure ±20%
  * Noise 추가
  * Zoom-in (사이즈 작아질 때 robustness 강화)

---

## ✔️ Inference JSON 예시

```json
{
  "predictions": [
    {
      "class": "aphid",
      "confidence": 0.91,
      "x": 233,
      "y": 180,
      "width": 22,
      "height": 18
    },
    {
      "class": "egg",
      "confidence": 0.74,
      "x": 290,
      "y": 140,
      "width": 12,
      "height": 10
    }
  ]
}
```

---

## 🛠️ IoT 연동 로직 예시

| 해충 감지    | 자동 반응              |
| -------- | ------------------ |
| aphid    | 사용자 알림 + 잎 세척 가이드  |
| mite     | 환기 + LED 광량 조정     |
| scale    | "심각" 알림 → 즉시 조치 필요 |
| egg      | 모니터링 강화            |
| pest(기타) | 사진 저장 + 사용자 리뷰     |

**임계치 추천:**

* confidence ≥ 0.5 이상일 때 알림
* pest 개수 ≥ 3개 → “고위험” 경고

---

## 📂 폴더 구조 권장

```
/roboflow/pest-detection/
    /dataset/
    /export/
    classes.txt
```

---

## 📌 결론

해충 감지 모델은 스마트 가드닝에서 **가장 난이도 있지만 가치가 높은 모델**이다.
초기에는 2~3종만 탐지해도 실사용 효과는 매우 크다.
데이터만 충분하면 YOLO 기반으로 높은 정확도 확보 가능하다.

---
