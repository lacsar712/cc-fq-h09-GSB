"""Pytest fixtures: isolated sqlite app + authenticated client.

DATABASE_URL must point at sqlite before app.config is imported.
"""
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./.pytest_fastq.db")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import Job, JobStage, Sample


GOOD_FASTQ = """@SEQ1
ACGTACGT
+
IIIIHHHH
@SEQ2
NNNNACGT
+
IIIIIIII
"""


@pytest.fixture()
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def bioops_headers(client):
    resp = client.post(
        "/api/auth/login", json={"username": "bioops", "password": "fastq123456"}
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def sample_ids(db):
    good = Sample(
        name="test-good",
        description="合格样例",
        is_broken=False,
        fastq_content=GOOD_FASTQ,
    )
    blank = Sample(
        name="test-blank",
        description="空内容样例",
        is_broken=False,
        fastq_content=" \n\t ",
    )
    db.add_all([good, blank])
    db.commit()
    return {"good": good.id, "blank": blank.id}
