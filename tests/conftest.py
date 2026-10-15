"""pytest 공통 픽스처."""

from __future__ import annotations

import pytest
import pytest_asyncio

from app.config import Config
from app.db import Database


@pytest.fixture
def config(tmp_path) -> Config:
    return Config(bot_token="123456:TEST-TOKEN", db_path=str(tmp_path / "bot.db"))


@pytest_asyncio.fixture
async def db(tmp_path):
    database = Database(tmp_path / "test.db")
    await database.connect()
    yield database
    await database.close()
