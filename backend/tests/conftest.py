"""Pytest fixtures: isolated SQLite DB + authenticated FastAPI test client.

DATABASE_URL must point at SQLite before ``app.*`` is imported, so this
module sets it at top level.
"""

import os
import tempfile

_TEST_DB = os.path.join(tempfile.gettempdir(), "fastq_qc_test.sqlite")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{_TEST_DB}")
os.environ.setdefault("JWT_SECRET", "fastq-qc-pipeline-test-secret")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Job, JobStage, Sample  # noqa: E402


GOOD_FASTQ = """@SEQ1
ACGTACGT
+
IIIIHHHH
@SEQ2
NNNNACGT
+
IIIIIIII
"""


@pytest.fixture(scope="session")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Clean tables before each test and expose a session."""
    session = SessionLocal()
    session.query(JobStage).delete()
    session.query(Job).delete()
    session.query(Sample).delete()
    session.commit()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def bioops_token(client):
    resp = client.post(
        "/api/auth/login", json={"username": "bioops", "password": "fastq123456"}
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers(bioops_token):
    return {"Authorization": f"Bearer {bioops_token}"}
