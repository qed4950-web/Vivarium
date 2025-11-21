# 🌱 Soil Condition Detection Model Guide

스마트 가드닝 프로젝트 — 토양 표면 상태 감지 모델

이 문서는 토양의 **건조·과습·곰팡이·변색** 등을 자동 감지하기 위한 Roboflow 기반 모델 개발 가이드입니다.

---

## 📌 모델 목표

카메라로 촬영된 토양 이미지를 분석하여 다음 상태를 자동 판정한다:

* **dry** (건조)
* **wet** (적당히 촉촉)
* **overwatered** (심한 과습, 물 고임)
* **mold** (흰 곰팡이)
* **moss** (이끼)
* **foreign-object** (벌레·이물질 등)

이는 센서(토양 수분센서)로는 절대 감지할 수 없는 **표면 시각 정보**를 보완하기 위해 필요하다.

---

## 📁 Dataset 구성

토양은 표면 상태가 명확하므로 **Classification 모델**로 충분함.

```
classes:
  - dry
  - wet
  - overwatered
  - mold
  - moss
  - foreign
```

---

## 📸 데이터 수집 팁

### 1) 조명 다양화

* LED 아래
* 밤/낮
* 음영진 곳
* 토양 위 광반사 상황 포함

### 2) 다양한 물주기 상태 촬영

* 물 준 직후
* 3시간 후
* 6시간 후
* 완전 건조 단계

### 3) 토양 표면 가까이 클로즈업

* 5~15cm 거리 추천
* 곰팡이/이끼는 근접 촬영 중요

---

## 🔖 Annotation 방식

* 기본: **Classification**
* 특별한 이물질(벌레, 쓰레기 등)을 잡고 싶다면
  → `foreign-object` 클래스로 추가
* 실제 운영에서는 Classification이 매우 안정적임

---

## 🧪 학습 설정 추천

Roboflow Train:

* **Model:** YOLO11-cls (가벼우면서 강력)
* **Image Size:** 416
* **Augmentations:**

  * Flip Horizontal
  * Crop ±10%
  * Exposure ±15%
  * Blur (소량)
  * Noise (토양 질감 robustness 강화)

---

## ✔️ Inference 결과 예시

```json
{
  "prediction": "mold",
  "confidence": 0.88
}
```

---

## 🛠️ IoT 제어 로직 예시

예: `soil_status` 값에 따라 자동 반응

| soil_status | 자동 제어                |
| ----------- | -------------------- |
| dry         | 펌프 20–40초 가동         |
| wet         | 정상 → 아무 동작 없음        |
| overwatered | 환기팬 증가, 다음 물 주기 제한   |
| mold        | 펜/환기 5분, 사용자 알림      |
| moss        | 광량/습도 과다 가능 → LED 조정 |

---

## 🧱 파일 구조 예시

```
/roboflow/soil-condition/
    /dataset/
    /export/
    classes.txt
```

---

## 📌 결론

토양 표면 상태 모델은 **센서 데이터의 약점을 보완하는 핵심 모델**이다.
특히 **곰팡이/이끼/과습**은 센서가 절대 감지할 수 없기 때문에
스마트 가드닝 자동화에서 필수적인 컴포넌트다.

---
