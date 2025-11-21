# 🖥️ 스마트 가드닝 AIoT

## **Python 추론 서버 가이드라인 (Inference Server Guideline)**

Roboflow/YOLO 모델을 Python에서 실시간 추론 → API → IoT 장치로 전달하는 전체 흐름

---

# 🎯 1. 목적

이 문서는 스마트 가드닝 시스템에서 **AI 모델을 실시간으로 추론**하고
그 결과를 ESP32/아두이노 등 IoT 장치에 전달하기 위한
**Python 기반 추론 서버 구축 기준**을 제공한다.

* YOLO 모델 로드
* 이미지 입력 처리
* 추론 결과 정리
* API 서버(FastAPI/Flask) 구성
* ESP32로 메시지 전달 구조
* 운영 시 최적화 전략

---

# 🧩 2. 시스템 개요

```
[Camera] → [Python 추론 서버] → [검출 결과] → [ESP32 제어]
```

Python 서버는 다음을 수행한다:

1. 카메라 또는 이미지 파일 입력 받아 처리
2. YOLO 모델로 병반/건강/벌레 예측
3. 결과 → JSON 형태로 제공(API)
4. 필요 시 ESP32/Aduino 컨트롤 명령 전송

---

# 📦 3. 설치 및 환경 구성

### Python 기본 패키지 설치

```bash
pip install ultralytics
pip install fastapi uvicorn
pip install opencv-python
pip install paho-mqtt     # (MQTT 사용 시)
pip install pyserial      # (Serial 연결 시)
```

---

# 🤖 4. YOLO 모델 로드 코드 (기본)

### `inference.py`

```python
from ultralytics import YOLO
import cv2

# 모델 로드
model = YOLO("best.pt")   # Roboflow에서 export한 YOLO11/YOLOv8 모델

def run_inference(image_path):
    img = cv2.imread(image_path)
    results = model(img)[0]

    detections = []
    for box in results.boxes:
        cls = int(box.cls[0])
        label = results.names[cls]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detections.append({
            "label": label,
            "confidence": conf,
            "box": [x1, y1, x2, y2]
        })

    return detections
```

---

# 🌐 5. FastAPI 기반 추론 서버 구성

### `server.py`

```python
from fastapi import FastAPI, UploadFile, File
from inference import run_inference
import shutil
import uuid

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # temp 저장
    temp_name = f"/tmp/{uuid.uuid4()}.jpg"
    with open(temp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = run_inference(temp_name)

    return {"detections": results}
```

### 서버 실행

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

---

# 📸 6. 실시간 영상 처리(카메라 스트림)

```python
import cv2
from inference import model

cap = cv2.VideoCapture(0)  # 웹캠

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    # 처리 로직 추가
```

---

# 📡 7. ESP32/아두이노 연동 옵션 3가지

---

## ✔ (1) Serial 연동 (USB)

Python → ESP32로 신호 전송

```python
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200)

def send_cmd(cmd):
    ser.write((cmd + "\n").encode())
```

예:

```python
if "brown_spot" in detected_labels:
    send_cmd("SPRAY_ON")
```

---

## ✔ (2) HTTP 연동 (WiFi)

```python
import requests
requests.get("http://192.168.0.50/pump/on")
```

---

## ✔ (3) MQTT 연동 (IoT 표준)

```python
import paho.mqtt.client as mqtt
mqttc = mqtt.Client()
mqttc.connect("192.168.0.10", 1883)
mqttc.publish("garden/control", "spray=on")
```

ESP32는 `client.subscribe("garden/control")`로 받음.

---

# 🧠 8. 스마트 가드닝 로직 예시

예시: 병반 감지 → 분무 / 건조 → 급수

```python
labels = [d["label"] for d in detections]

if "leaf_mold" in labels:
    send_cmd("FAN_ON")

if "dry_leaf" in labels:
    send_cmd("PUMP_ON")
```

또는 식물 스트레스 기반 자동 조절:

```python
if "yellowing_leaf" in labels:
    increase_light()
```

---

# ⚡ 9. 최적화 전략

### ⏱ 지연/안전 기준

* end-to-end 추론(입력~응답) 목표: 1초 이내, 최대 2초 초과 시 알림 로그 남기기(uvicorn access log 확인).
* 매 요청 후 temp 파일은 `os.remove(temp_name)` 등으로 삭제해 디스크 누적을 방지.
* 카메라 스트림은 FPS를 제한(예: 5~10fps)해 모델 지연과 발열을 줄인다.

### ✔ 이미지 Crop

화분 영역만 추출 후 YOLO 실행 → 속도 2~3배 증가

### ✔ Batch 추론

여러 화분 이미지 동시처리 가능

### ✔ FP16 가속

GPU 있으면 `model.to("cuda").half()`

### ✔ Tiny 모델 사용

YOLO11n or YOLO8n → Edge 환경 완전 최적화

---

# 🛠 10. 운영 체크리스트

* [ ] 모델 파일(best.pt or .onnx) 정상 로드
* [ ] API 서버 8000 포트 정상 작동
* [ ] 카메라 입력 때 프레임 드랍 없는지 확인
* [ ] ESP32/Serial 연결 안정성 체크
* [ ] 예외 처리(파일 오류/카메라 오류) 넣기

---

# 🚀 11. 다음 단계

이제 AI 추론 서버까지 준비됨.

다음 문서는 **Arduino/ESP32 연동 가이드라인**이다.

📄 다음 파일: **07_Arduino_ESP32_연동_가이드라인.md**
