import os
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

os.environ.setdefault("TRADING_MODE", "DEMO")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{ROOT / 'data' / 'test.db'}")
os.environ.setdefault("SECRET_KEY", "test")


@pytest.fixture(scope="session", autouse=True)
def demo_data():
    script = ROOT / "backend" / "scripts" / "generate_demo_parquet.py"
    subprocess.check_call([sys.executable, str(script)], cwd=str(ROOT / "backend"))


@pytest.fixture()
def db_session():
    from app.db import Base

    engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
