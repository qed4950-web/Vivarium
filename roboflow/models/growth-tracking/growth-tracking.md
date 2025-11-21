# 🌿 Growth Tracking & Segmentation Model Guide

스마트 가드닝 프로젝트 — 성장 측정 / 잎·줄기 세그멘테이션 모델

이 문서는 식물의 **성장 속도, 잎 면적, 줄기 길이, 잎 개수 변화** 등을 자동으로 측정하는
Roboflow 기반 **Segmentation / Detection 모델** 구축 가이드이다.

---

## 📌 모델 목표

카메라로 촬영된 식물 이미지에서 다음 요소들을 자동 분석한다:

* 식물 전체 영역 Mask (Plant Mask)
* 잎 개수 추정
* 잎 면적(픽셀 단위 → cm² 환산)
* 줄기 길이 변화
* 시간 경과(Time-lapse)에 따른 성장 속도 계산

이 기능은 사용자에게 “성장 그래프”를 제공하고,
자동 물주기/광량 조절 로직 개선에도 사용된다.

---

## 🧩 왜 Segmentation인가?

성장을 측정하려면 **정확한 모양(경계선) 정보**가 필요하다.

* Detection(박스) → 대략적인 크기만 측정
* **Segmentation(Mask)** → 실제 잎/줄기 면적까지 정확히 계산 가능

따라서 **Instance Segmentation**이 최적이지만
초기에는 **Semantic Segmentation** 한 가지 클래스(plant)로도 가능하다.

---

## 📁 Dataset 구조

```
classes:
  - plant
```

원한다면 다음처럼 세분화도 가능:

```
classes:
  - leaf
  - stem
  - background
```

**하지만 MVP는 plant 단일 클래스 권장.**

---

## 📸 데이터 수집 팁

### 1) 정면, 상단 위주 촬영

* 항상 같은 각도/거리 유지하면 성장 측정 정확도 ↑

### 2) 일관된 조명 환경

* LED 키트 사용 시 일정한 색 온도로 유지

### 3) 같은 식물을 여러 날짜에 촬영

* Time-lapse 모델 학습에 사용됨

### 4) 배경은 단순할수록 좋음

* 식물 중심 segmentation 실패 확률 ↓

---

## 🔖 Annotation 방식

Roboflow Annotate에서:

* **Polygon** 툴로 식물 전체 윤곽을 따기
* 잎 단위 segmentation 필요하면 Instance Segmentation 활성화
* 단일 mask 데이터만으로도 충분히 유용

---

## 🧪 학습 설정 추천

### 옵션 1) Semantic Segmentation (MVP)

* 모델: **YOLO11-seg / YOLOv8-seg**
* 클래스: `plant`
* 목적: 식물 전체 mask → 면적 계산

### 옵션 2) Instance Segmentation (고급)

* 모델: **YOLO11-seg-large**
* 목적: 잎 개수 추정, 잎별 길이/면적 계산

---

## 📊 출력 예시 (SemSeg)

```json
{
  "mask": "base64_encoded_mask",
  "area_px": 204312,
  "plant_percentage": 0.34
}
```

면적을 실제 cm²로 환산하려면
“픽셀 → 실제 거리 변환 비율(calibration)”이 필요함.

---

## 📈 성장 분석 로직 (예시)

### 1) 면적 계산

```
area_cm2 = area_px * pixel_to_cm_ratio
```

### 2) 성장률 계산

```
growth_rate = (today_area - yesterday_area) / yesterday_area
```

### 3) 잎 개수 변화(Instance Seg)

* segmentation mask count = 잎 개수

### 4) 줄기 길이 변화

* 줄기 세그멘테이션 시 skeletonize → 길이 추정

---

## 🪴 IoT 연동 아이디어

| 성장 변화    | 자동 제어             |
| -------- | ----------------- |
| 성장 정체    | 조도 증가, 물 공급 패턴 조정 |
| 잎 면적 감소  | 병충해/광량 부족 가능 → 알림 |
| 과도한 성장   | LED/물 공급 과다 여부 검사 |
| 성장 속도 급감 | 온습도 환경 점검         |

---

## 🧱 파일 구조 권장

```
/roboflow/growth-tracking/
    /dataset/
    /export/
    segmentation-config.json
```

---

## 📌 결론

성장 추적 모델은 스마트 가드닝의 “스마트함”을 극대화하는 고급 기능이다.
초기에는 단일 plant mask만으로도 충분히 유용하며,
차후 인스턴스 세그멘테이션으로 확장하면 잎 단위 성장 분석까지 가능하다.

---
