# 🌱 Smart Gardening AIoT — Roboflow Vision System (Index)

스마트 가드닝 프로젝트에서 사용하는 **4개의 비전 AI 모델** 문서를 정리한 메인 인덱스입니다.
각 문서는 독립적으로 사용 가능하며, Roboflow 기반 데이터셋·학습·배포 가이드 포함.

---

## 📦 포함된 문서

### 1. [Leaf Health Detection](leaf-health.md)

식물 잎의 **변색 / 반점 / 갈변 / 말림 / 노화** 등을 자동 분석하는 모델

* Classification 기반
* LED/물주기/환기 자동 제어와 연동
* 초기 이상 징후를 가장 빠르게 감지하는 핵심 모델

---

### 2. [Soil Condition Detection](soil-condition.md)

토양 표면의 **건조 / 과습 / 곰팡이 / 이끼 / 이물질** 상태를 감지

* 센서가 절대 판별할 수 없는 부분을 커버
* 물 주기 제어 로직의 정확도를 크게 향상
* Classification 기반

---

### 3. [Pest Detection](pest-detection.md)

응애, 진딧물, 깍지벌레, 유충 등 **해충 객체 탐지 모델**

* YOLO 기반 Object Detection
* 작은 벌레도 bounding box로 검출
* 위험도 기반 자동 알림 시스템과 연동

---

### 4. [Growth Tracking & Segmentation](growth-tracking.md)

식물의 **성장 속도 / 잎 면적 / 잎 개수 / 줄기 길이** 자동 분석

* Segmentation (semantic / instance)
* 성장 그래프, 타임랩스 분석, 환경 튜닝에 활용

---

## 🔗 프로젝트 구조

```
/roboflow/
    index.md
    leaf-health.md
    soil-condition.md
    pest-detection.md
    growth-tracking.md
```

---

## 🎯 전체 시스템 요약

| 영역 | 센서 데이터       | 비전 AI (Roboflow) | 목적         |
| -- | ------------ | ---------------- | ---------- |
| 잎  | 밝기/온도와 간접 관련 | ✔ 잎 변색·반점·말림     | 건강 상태 판단   |
| 토양 | 습도 센서만 가능    | ✔ 표면 곰팡이/변색/건조   | 물주기 정확도 강화 |
| 해충 | ✖ 불가능        | ✔ 해충 Detection   | 병충해 조기 대응  |
| 성장 | ✖ 불가능        | ✔ segmentation   | 성장 그래프 생성  |

---

## 🚀 추천 적용 순서(MVP → Final)

1. 토양 상태 감지
2. 잎 건강 감지
3. 해충 감지
4. 성장 분석

---

## 📌 마지막 한 줄 요약

이 문서 세트는 “센서 + 비전 AI”를 결합한 **완전 자동 스마트 가드닝 시스템**을 구축하기 위한 전체 로드맵이다.

---
