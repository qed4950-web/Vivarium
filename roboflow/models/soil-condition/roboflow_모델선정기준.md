스마트 가드닝에서 필요한 Soil 모델은 보통:

흙 상태 감지

촉촉한지 / 건조한지

표면 색으로 토양 수분 추정

흙 종류 분류

Clay / Loamy / Sandy 등

흙 품질 분석

질소/인/칼륨(NPK) 지표, 영양 상태
(카메라 기반이라 정확도는 한계가 있지만 일부 모델은 실험적 지원)

토양 위 물웅덩이, 곰팡이, 오염 등 감지

# SoilAI Guides (Combined)

## 1. soil_model_guide.md

### 🌱 SoilAI 모델 가이드 (soilai/5)

#### 1. 모델 개요

* **모델명:** soilai/5
* **모델 타입:** ResNet34 Multi-label Classification
* **정확도:** Validation Accuracy 90.9%
* **학습 데이터:** 1,368장
* **라벨:** NPK 영양 레벨 (N0/N1, P0/P1, K0/K1)

#### 2. 모델이 무엇을 판단하나?

| 라벨           | 의미    | 제어 방향    |
| ------------ | ----- | -------- |
| **N0**       | 질소 부족 | 질소 비료 투입 |
| **P0**       | 인산 부족 | 인 비료 투입  |
| **K0**       | 칼륨 부족 | 칼륨 비료 투입 |
| **N1/P1/K1** | 정상    | 유지       |

#### 3. API 호출 예시 (Python)

```python
from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ROBOFLOW_PRIVATE_KEY"
)

result = client.infer("soil.jpg", model_id="soilai/5")
print(result)
```

#### 4. 예측 결과 예시(JSON)

```json
{
  "predictions": {
    "K1": { "confidence": 0.954 },
    "N0": { "confidence": 0.97 },
    "P1": { "confidence": 0.997 }
  }
}
```

---

## 2. python_연동가이드.md

### 🐍 Python SoilAI 연동 가이드

#### 1. 요구사항 설치

```bash
pip install fastapi uvicorn inference-sdk python-multipart
```

#### 2. FastAPI 서버 코드

```python
from fastapi import FastAPI, UploadFile
from inference_sdk import InferenceHTTPClient

app = FastAPI()

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ROBOFLOW_PRIVATE_KEY"
)

@app.post("/infer")
async def infer_image(file: UploadFile):
    image_bytes = await file.read()
    result = client.infer(image_bytes, model_id="soilai/5")
    return result
```

#### 3. 서버 실행

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

#### 4. ESP32 → 서버 요청 예시

```cpp
HTTPClient http;
http.begin("http://192.168.0.10:8000/infer");
http.addHeader("Content-Type", "image/jpeg");
int res = http.POST(camera_fb->buf, camera_fb->len);
```

---

## 3. ESP32→서버→SoilAI 흐름도.md

### 📡 ESP32 → 서버(MacBook) → SoilAI 전체 흐름도

```
ESP32-CAM
   ↓ (JPEG 이미지)
Python Server (FastAPI)
   ↓ (Inference API)
Roboflow SoilAI Model
   ↓ (NPK 분석 결과)
Python Server
   ↓
ESP32 제어
```

### 단계별 상세 설명

#### 1) ESP32가 사진 캡처

* 카메라 프레임 → JPEG 변환
* 서버로 HTTP POST 전송

#### 2) Python 서버가 이미지 수신

* `/infer`에서 이미지 처리
* SoilAI API 호출

#### 3) SoilAI 모델 예측

* NPK 부족/정상 상태 분석

#### 4) ESP32 제어

* 비료/물/환기 자동 제어

---

필요하면 **각 문서를 실제 독립 파일로 분리**해서 따로 생성해줄게!
