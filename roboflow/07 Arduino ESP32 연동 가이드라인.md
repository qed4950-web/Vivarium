# 🔌 스마트 가드닝 AIoT

## **Arduino / ESP32 연동 가이드라인 (MCU Integration Guideline)**

Python 추론 서버 → MCU(ESP32/Arduino) 제어 통신 규칙 및 코드 템플릿

---

# 🎯 1. 목적

이 문서는 AI 모델이 감지한 결과에 따라
**급수(Pump), 조명(LED), 환기(Fan), 분무(Mist) 등의 장치를 제어**하기 위해
`Python ↔ ESP32/Arduino` 간 통신 구조를 명확히 정의한다.

지원 프로토콜:

1. **Serial (USB)**
2. **WiFi HTTP (REST)**
3. **MQTT (IoT 표준)**

---

# 🧩 2. 전체 시스템 구조

```
[Camera]
   │
[Python AI Server]
   │  (결과 전달)
   ▼
[ESP32 / Arduino MCU]
   │
   ├─ Pump ON/OFF
   ├─ LED Grow Light ON/OFF
   ├─ Fan ON/OFF
   ├─ Humidifier / Mist ON/OFF
```

MCU는 "명령 처리"만 하고
AI 판단은 Python이 담당한다.

---

# 🔌 3. Serial(USB) 연결 가이드 (가장 간단)

## ✔ Python → ESP32/Arduino

### Python 코드

```python
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)

def send_cmd(cmd):
    ser.write((cmd + "\n").encode())
```

예시:

```python
send_cmd("PUMP_ON")
send_cmd("PUMP_OFF")
```

---

## ✔ ESP32(Arduino) 코드

```cpp
void setup() {
  Serial.begin(115200);
  pinMode(4, OUTPUT);  // Pump
  pinMode(5, OUTPUT);  // LED
  pinMode(6, OUTPUT);  // Fan
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "PUMP_ON") digitalWrite(4, HIGH);
    if (cmd == "PUMP_OFF") digitalWrite(4, LOW);

    if (cmd == "LED_ON") digitalWrite(5, HIGH);
    if (cmd == "LED_OFF") digitalWrite(5, LOW);

    if (cmd == "FAN_ON") digitalWrite(6, HIGH);
    if (cmd == "FAN_OFF") digitalWrite(6, LOW);
  }
}
```

---

# 🌐 4. WiFi HTTP 연동 가이드 (무선 제어)

### Python HTTP 요청

```python
import requests
requests.get("http://192.168.0.50/pump/on")
```

---

## ✔ ESP32(HTTP 서버)

```cpp
#include <WiFi.h>
#include <WebServer.h>

WebServer server(80);

void setup() {
  WiFi.begin("SSID", "PASS");
  pinMode(4, OUTPUT);
  server.on("/pump/on", []() {
    digitalWrite(4, HIGH);
    server.send(200, "text/plain", "pump_on");
  });
  server.on("/pump/off", []() {
    digitalWrite(4, LOW);
    server.send(200, "text/plain", "pump_off");
  });
  server.begin();
}

void loop() {
  server.handleClient();
}
```

---

# 📡 5. MQTT 연동 가이드 (가장 강력, IoT 표준)

## ✔ Python MQTT Publisher

```python
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.connect("192.168.0.10", 1883)

mqttc.publish("garden/pump", "on")
mqttc.publish("garden/light", "off")
```

---

## ✔ ESP32 MQTT Subscriber

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)payload[i];

  if (String(topic) == "garden/pump") {
    if (msg == "on") digitalWrite(4, HIGH);
    if (msg == "off") digitalWrite(4, LOW);
  }
}

void setup() {
  WiFi.begin("SSID", "PASS");
  client.setServer("192.168.0.10", 1883);
  client.setCallback(callback);
  client.subscribe("garden/pump");
}

void loop() {
  client.loop();
}
```

---

# 🧠 6. 스마트 가드닝 자동화 로직 예시

### 예: 병반 감지 → 팬 가동

Python:

```python
if "leaf_mold" in labels:
    send_cmd("FAN_ON")
```

### 예: 건조 잎 발견 → 급수

```python
if "dry_leaf" in labels:
    send_cmd("PUMP_ON")
```

### 예: 식물 성장 느림 → 광량 증가

```python
if "stressed_leaf" in labels:
    send_cmd("LED_ON")
```

---

# ⚠️ 7. MCU 제어 시 주의사항

### ✔ 1) 릴레이가 HIGH / LOW 반전되는 보드주의

일부 릴레이는 LOW = ON
문서 확인 필요

### ✔ 2) 펌프/팬은 외부 5V 전원 사용

ESP의 3.3V 핀에 직접 연결 절대 금지

### ✔ 3) 모든 장치는 **공통 GND** 필수

### ✔ 4) MOSFET 추천 모델

IRLZ44N, AO3400
(3.3V에서 안정적으로 게이트 ON 가능)

### ✔ 5) 타이머 포함 명령 사용 (안전)

Python → MCU 명령에 시간 정보를 포함하면 사고를 줄일 수 있음.

예) `PUMP_ON:3000` (3초 후 자동 OFF)

```cpp
// 명령 예: "PUMP_ON:3000"
if (cmd.startsWith("PUMP_ON")) {
  int sep = cmd.indexOf(':');
  int duration = (sep > 0) ? cmd.substring(sep + 1).toInt() : 0;
  digitalWrite(4, HIGH);
  if (duration > 0) {
    delay(duration);
    digitalWrite(4, LOW);  // 안전 자동 OFF
  }
}
```

---

# 🔍 8. 운영 체크리스트

* [ ] Python → MCU 통신 정상
* [ ] 릴레이/모터 ON/OFF 정확
* [ ] 장시간 운영 시 발열 없음
* [ ] MCU WiFi 안정적
* [ ] 명령 수신 지연 없음

---

# 🚀 9. 다음 단계

이제 Python 서버도, MCU 연동도 끝났어.
마지막 단계인 **자동화 로직 전체 운영(Automation Flow) 가이드라인**이 남아있어.

📄 다음 파일: **08_전체_운영_로직_가이드라인.md**
