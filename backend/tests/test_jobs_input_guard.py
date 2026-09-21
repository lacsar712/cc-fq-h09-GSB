"""API-level guard tests for POST /api/jobs (server is the final defense)."""

from app.models import Job, Sample


GOOD_FASTQ = """@SEQ1
ACGTACGT
+
IIIIHHHH
@SEQ2
NNNNACGT
+
IIIIIIII
"""


def _make_sample(db, *, name, content, is_broken=False):
    sample = Sample(
        name=name,
        description="test",
        is_broken=is_broken,
        fastq_content=content,
    )
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample


def test_empty_paste_rejected(client, auth_headers, db):
    resp = client.post("/api/jobs", json={"fastqText": ""}, headers=auth_headers)
    assert resp.status_code == 400
    assert db.query(Job).count() == 0


def test_whitespace_paste_rejected(client, auth_headers, db):
    resp = client.post(
        "/api/jobs", json={"fastqText": "  \n\t  "}, headers=auth_headers
    )
    assert resp.status_code == 400
    assert db.query(Job).count() == 0


def test_missing_input_rejected(client, auth_headers, db):
    resp = client.post("/api/jobs", json={}, headers=auth_headers)
    assert resp.status_code == 400
    assert db.query(Job).count() == 0


def test_empty_sample_rejected(client, auth_headers, db):
    sample = _make_sample(db, name="blank-empty", content="")
    resp = client.post(
        "/api/jobs", json={"sampleId": sample.id}, headers=auth_headers
    )
    assert resp.status_code == 400
    assert "样例内容为空" in resp.json()["detail"]
    assert db.query(Job).count() == 0


def test_whitespace_sample_rejected(client, auth_headers, db):
    sample = _make_sample(db, name="blank-ws", content="  \n ")
    resp = client.post(
        "/api/jobs", json={"sampleId": sample.id}, headers=auth_headers
    )
    assert resp.status_code == 400
    assert db.query(Job).count() == 0


def test_valid_paste_starts_run(client, auth_headers, db):
    resp = client.post(
        "/api/jobs", json={"fastqText": GOOD_FASTQ}, headers=auth_headers
    )
    assert resp.status_code == 201, resp.text
    job_id = resp.json()["id"]

    job = db.query(Job).filter(Job.id == job_id).first()
    assert job is not None
    assert job.status == "success"
    assert job.fastq_snapshot.strip()
    stage_names = {s.actor_name: s.status for s in job.stages}
    assert stage_names["ParseActor"] == "success"
    assert stage_names["ReportActor"] == "success"


def test_valid_sample_starts_run(client, auth_headers, db):
    sample = _make_sample(db, name="good-one", content=GOOD_FASTQ)
    resp = client.post(
        "/api/jobs", json={"sampleId": sample.id}, headers=auth_headers
    )
    assert resp.status_code == 201, resp.text
    job = db.query(Job).filter(Job.id == resp.json()["id"]).first()
    assert job.status == "success"
    assert job.sample_id == sample.id


def test_unauthenticated_request_rejected(client, db):
    resp = client.post("/api/jobs", json={"fastqText": GOOD_FASTQ})
    assert resp.status_code == 401
    assert db.query(Job).count() == 0
