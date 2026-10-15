# bot-kit — 24/7 텔레그램 봇 스타터 킷

[![CI](https://github.com/dashcloud-kr/bot-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/dashcloud-kr/bot-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

`python-telegram-bot` v22 + SQLite(WAL) + pytest + GitHub Actions로 구성된 **프로덕션용 텔레그램 봇 스타터 킷**입니다.
[대시클라우드(DashCloud)](https://dashcloud.kr)에서 **평생 무료로 24시간 가동**하는 것을 기준으로 만들었습니다.

> **English** — A production-ready Telegram bot starter kit: `python-telegram-bot` v22, SQLite persistence with migrations, graceful shutdown, error handling, pytest harness and CI. Built to run 24/7 on [DashCloud](https://dashcloud.kr) for free.

## 들어있는 것

| 구성 | 설명 |
| --- | --- |
| 롱폴링 부트스트랩 | 인바운드 포트·도메인·웹훅 설정 없이 바로 동작 |
| Graceful shutdown | 컨테이너 종료 신호(SIGTERM)에서 안전하게 정리 후 종료 |
| SQLite 영구 저장 | WAL 모드 + `PRAGMA user_version` 순차 마이그레이션 |
| 공통 명령어 | `/start` `/help` `/status` `/id` |
| 전역 오류 핸들러 | 로그 기록 + `ADMIN_CHAT_ID`로 오류 알림(선택) |
| 긴 메시지 분할 | 4096자 제한 자동 분할 유틸 (`chunk_text`) |
| 테스트 하네스 | pytest + pytest-asyncio + respx, PTB Update 팩토리 포함 |
| CI | GitHub Actions에서 ruff + pytest 자동 실행 |
| 배포 매니페스트 | `dashcloud.json` (원클릭 배포용) |

## 30초 로컬 실행

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# .env 에 TELEGRAM_BOT_TOKEN 입력 — 텔레그램 @BotFather 에서 발급

python bot.py
```

## DashCloud로 24시간 무료 가동

1. [dashcloud.kr](https://dashcloud.kr) 가입 — 휴대폰 인증 1회, 결제 정보 불필요
2. 이 폴더를 대시보드에 **드래그 앤 드롭** (또는 Git 저장소 연동)
3. 프로젝트 설정 → 환경변수에 `TELEGRAM_BOT_TOKEN` 등록
4. 배포 — `dashcloud.json`이 런타임(Python 3.12)과 진입점을 자동 설정합니다

> 노트북을 덮어도, 터미널을 꺼도 봇이 계속 돌아갑니다. Free 플랜은 평생 무료이며 갱신·슬립이 없습니다.

## 구조

```
bot-kit/
├── bot.py                  # 엔트리포인트 (run_polling)
├── app/
│   ├── config.py           # 환경변수 로딩·검증
│   ├── db.py               # SQLite 헬퍼 + 마이그레이션
│   ├── bot.py              # Application 팩토리 (핸들러/수명주기/오류)
│   ├── handlers/common.py  # 공통 명령어
│   └── utils/text.py       # 메시지 분할 유틸
├── tests/                  # pytest (팩토리 포함)
├── dashcloud.json          # 배포 매니페스트
└── .github/workflows/ci.yml
```

## 새 봇 만들기

1. 이 킷을 복사해 새 레포로 시작
2. `app/handlers/`에 기능 핸들러 추가
3. `bot.py`에서 등록:

```python
from app.bot import build_application
from app.config import Config
from app.handlers.my_feature import my_handler  # 새 핸들러

application = build_application(
    config,
    migrations=["CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, keyword TEXT);"],
    extra_handlers=[my_handler],
)
```

4. 외부 API 클라이언트는 `app/clients/`에 두고 `httpx`로 작성 — 테스트에서는 `respx`로 모킹합니다

## 테스트

```bash
pip install -r requirements-dev.txt
ruff check . && pytest -q
```

## 라이선스

[MIT](LICENSE) — 자유롭게 복사·수정·배포하세요.
