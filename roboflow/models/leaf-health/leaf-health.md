# 🌿 Leaf Health Detection Model Guide

스마트 가드닝 프로젝트 — 잎 건강 상태 분석 모델

이 문서는 식물 잎의 **건강 상태를 자동 분석**하는 Roboflow 기반 모델 개발 가이드입니다.

---

## 📌 모델 목표

카메라로 촬영된 식물 잎 이미지에서 다음 상태를 자동 판단한다:

* **정상 잎 (healthy)**
* **노랗게 변한 잎 (yellowing)**
* **갈변 또는 타들어감 (browning / burning)**
* **반점·질병 패턴 (spot / disease)**
* **말림 (curling)**

문제의 원인까지 직접 판정하는 것이 아니라
**이상 징후를 빠르게 탐지**하는 것이 목적.

---

## 📁 Dataset 구성

추천 클래스 구조:

```
classes:
  - healthy
  - yellow
  - brown
  - spot
  - curl
```

### 데이터 수량 가이드

| 클래스     | 최소 권장 수량 |
| ------- | -------- |
| healthy | 80–100   |
| yellow  | 40–60    |
| brown   | 40–60    |
| spot    | 40–80    |
| curl    | 30–50    |

총 250~350장으로도 1차 MVP 모델 가능.

---

## 📸 데이터 수집 팁

1. **조명 다양화**

   * 자연광
   * LED 백색광
   * 밤 / 약한 조명
2. **각도 다양화**

   * 정면
   * 약간 비스듬히
3. **거리 다양화**

   * 전체 식물
   * 잎 클로즈업
4. **환경 다양화**

   * 배경이 복잡해도 괜찮음 (Roboflow Augmentation로 해결)

---

## 🔖 Annotation 방식 (권장)

* **Classification 모델** 추천
  → 사진 한 장 자체가 잎 상태를 판단하는 구조
* 여러 잎이 섞여 있는 경우
  → Object Detection 모델로 잎별 상태 라벨링 가능

초기 MVP는 Classification이 훨씬 빠르고 정확도 확보 쉬움.

---

## 🧪 모델 학습 설정

Roboflow Train에서 권장 옵션:

* **Model Type**:

  * *Classification — Fast model (MobileNet/YOLO11-cls)*
* **Image Size**: 416 or 512
* **Augmentations**:
  -.Rotate 0–15º
  -.Brightness ±20%
  -.Exposure ±20%
  -.Flip Horizontal
  -Crop 0–10%

---

## 🎛️ Inference 출력 예시(JSON)

```json
{
  "prediction": "yellow",
  "confidence": 0.92,
  "labels": {
    "healthy": 0.01,
    "yellow": 0.92,
    "brown": 0.03,
    "spot": 0.02,
    "curl": 0.02
  }
}
```

---

## 🪴 IoT 연동 로직 예시

* **yellow(노랗게)**
  → 조도 부족 or 질소 부족 → LED 밝기 증가
* **brown(갈변)**
  → 과습/과열 가능 → 환기 + 물 공급 중지
* **spot(반점)**
  → 곰팡이/병충해 위험 → 사용자 알림
* **curl(말림)**
  → 건조/과열 가능 → 가습 or Shade 조절

---

## 🧱 파일 구조 권장

```
/roboflow/leaf-health/
    /dataset/
    /export/
    classes.txt
    leaf-health-model.json (optional)
```

---

## 📌 결론

잎 건강 모델은 스마트 가드닝에서 **가장 먼저 구축해야 하는 핵심 모델**이다.
센서가 절대 감지하지 못하는 “식물의 시각적 SOS”를 자동 감지해주는 역할을 맡는다.

---
