# Repository Guidelines

## Project Structure & Module Organization
- Top-level: `roboflow/` holds the nine numbered guides (`00`–`08` plus `05_1`), contributor guide, and `프로젝트 폴더구조.md`; `업무현황/` holds cycle trackers.
- Inside `roboflow/models/`: per-model folders (`leaf-health`, `soil-condition`, `pest-detection`, `growth-tracking`) with guide markdown, dataset/export placeholders, and `classes.txt`.
- Keep numeric prefixes when editing or adding guides so ordering stays stable; match the existing heading/emojis pattern.
- Insert code samples and command snippets in the relevant guide; this repo is documentation-only.

## Work Cycle Tracking
- Track refactor cycles in `업무현황/README.md` using `cycle-XX` folders with `미완.md` and `완료.md`; move items from 미완 to 완료 each quarter and after project milestones.
- Carry forward only active items into the next `미완.md` and note dates/owners per task.

## Build, Test, and Development Commands
- No build step for markdown edits; preview locally.
- Training: `pip install ultralytics` then run the `YOLO("yolo11s.pt").train(...)` block in `roboflow/05 모델_학습 및 성능 향상 가이드라인.md`.
- Inference API: `pip install fastapi uvicorn opencv-python paho-mqtt pyserial` then `uvicorn server:app --host 0.0.0.0 --port 8000` from `roboflow/06 python 추론서버 가이드라인.md`.
- Device control: reuse Serial/HTTP/MQTT snippets in `roboflow/07 Arduino ESP32 연동 가이드라인.md`; document deviations.

## Coding Style & Naming Conventions
- Write concise, directive prose; use level-1/2 headings, short bullets, and fenced code blocks with language hints.
- Keep terminology aligned with the master guideline (Accuracy First, Real-Time Reaction, YOLO11/YOLOv8 naming).
- Preserve existing emoji section markers and numeric filename prefixes; keep Korean/English mixed labels consistent with neighboring files.

## Testing Guidelines
- No automated tests; dry-run new commands or code blocks in a clean Python 3.10+ environment.
- Align automation examples with `roboflow/00 마스터가이드라인.md` targets (e.g., <1s inference) and note required hardware near the sample.

## Commit & Pull Request Guidelines
- Use succinct, present-tense commit messages such as `docs: update inference server guide` or `docs: add labeling rules note`; group related edits in one commit.
- PRs should summarize scope, cite the guide(s) touched, and mention tested commands; include screenshots only when UI or visualization output is affected.
- Link issues or tasks when available and flag follow-up work (e.g., benchmarking or dataset version update).

## Security & Configuration Tips
- Do not commit Roboflow API keys, device credentials, or dataset exports; use placeholders and keep secrets in untracked env files.
- Keep AI decision logic decoupled from hardware control per `00 마스터가이드라인.md` (Python decides, ESP32 acts) and document any safety timer or lock changes.
