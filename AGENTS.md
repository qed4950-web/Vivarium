# Repository Guidelines

## Project Structure & Module Organization
- `roboflow/`: Nine numbered guides (`00`–`08` + `05_1`), contributor guide, and `index.md`.  
- `roboflow/models/`: Per-model folders (`leaf-health`, `soil-condition`, `pest-detection`, `growth-tracking`) with guide markdown plus `dataset/`, `export/`, `classes.txt` (and `masks/` for segmentation).  
- `업무현황/`: Cycle trackers (`cycle-XX/미완.md`, `완료.md`, `테스트플랜.md`) and `README.md` for process rules. Keep all new docs under `roboflow/`; keep operational tracking under `업무현황/`.

## Build, Test, and Development Commands
- No build step for docs; preview Markdown locally.  
- Training sample (see `roboflow/05...`):  
  - `pip install ultralytics`  
  - `python - <<'PY'\nfrom ultralytics import YOLO\nYOLO('yolo11s.pt').train(data='data.yaml', imgsz=640, epochs=100)\nPY`
- Inference API (see `roboflow/06...`):  
  - `pip install fastapi uvicorn opencv-python paho-mqtt pyserial`  
  - `uvicorn server:app --host 0.0.0.0 --port 8000`
- MCU control samples (see `roboflow/07...`): reuse Serial/HTTP/MQTT snippets; include timers (e.g., `PUMP_ON:3000`) for safety.
- Roboflow export/API (see 테스트플랜): `pip install roboflow`; use API key + project slug + version to download `yolov8`.

## Coding Style & Naming Conventions
- Use concise, directive prose; headings at level 1–2, short bullets, and fenced code blocks with language hints.
- Preserve numeric prefixes and existing emoji style; keep Korean/English mixed labels consistent.
- Filenames in `models/` should be kebab-case (e.g., `leaf-health.md`) with matching subfolders.

## Testing Guidelines
- No automated tests. Manually dry-run snippets in a clean Python 3.10+ env.
- Record command logs and outcomes in the relevant cycle `미완.md`/`완료.md`; note latency targets (<1s inference) and hardware assumptions (camera, ESP32 port, MQTT broker).

## Commit & Pull Request Guidelines
- Commit messages: short, present-tense (e.g., `docs: update inference guide`, `chore: add cycle checklist`).
- PRs: summarize scope, list touched files/paths (e.g., `roboflow/06...`, `업무현황/cycle-XX/...`), mention tested commands, and link issues/tasks when available.
- Group related doc edits into one commit; avoid mixing operational trackers and guide content changes without explaining in PR notes.

## Security & Configuration Tips
- Do not commit Roboflow API keys, dataset exports, or device credentials. Use placeholders and keep secrets in untracked env files.
- Keep AI logic separated from hardware control (Python decides, ESP32 acts) and always document safety timers/locks when modifying control examples.
