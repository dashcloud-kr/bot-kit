"""bot-kit 예제 봇 엔트리포인트.

DashCloud 배포 시 이 파일을 entrypoint 로 사용합니다.
"""

from __future__ import annotations

import logging

from dotenv import load_dotenv
from telegram import Update

from app.bot import build_application
from app.config import Config


def main() -> None:
    load_dotenv()
    config = Config.from_env()
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    application = build_application(config)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
