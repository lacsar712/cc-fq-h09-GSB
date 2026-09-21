"""Empty/whitespace FASTQ must never be enqueued; valid input still runs."""
import pytest

from app.EmptyInputGate import gate_paste, gate_sample
from app.models import Job


# ---------- guard unit tests ----------

@pytest.mark.parametrize("blank", [None, "", "   ", "\n\t ", " \r\n "])
def test_gate_paste_rejects_blank(blank):
    ok, text = gate_paste(blank)
    assert ok is False
    assert text == ""


@pytest.mark.parametrize("blank", [None, "", "   ", "\n\t "])
def test_gate_sample_rejects_blank(blank):
    ok, text = gate_sample(blank)
    assert ok is False
    assert text == ""


def test_gate_accepts_non_blank():
    ok_paste, text_paste = gate_paste("@r1\nACGT\n+\nIIII\n")
    assert ok_paste is True
    assert text_paste.startswith("@r1")

    ok_sample, text_sample = gate_sample(" @r1\nACGT\n+\nIIII\n ")
    assert ok_sample is True
    assert text_sample.startswith(" @r1")  # guard must not rewrite content


# ---------- API: paste path (server is the final line of defense) ----------

@pytest.mark.parametrize("payload", [
    {"fastqText": ""},
    {"fastqText": "   "},
    {"fastqText": "\n\t \r\n"},
    {},  # neither sampleId nor fastqText
])
def test_api_rejects_empty_paste(client, bioops_headers, db, payload):
    resp = client.post("/api/jobs", json=payload, headers=bioops_headers)
    assert resp.status_code == 400
    assert db.query(Job).count() == 0


def test_api_valid_paste_starts_and_runs(client, bioops_headers, db):
    payload = {"fastqText": "@SEQ1\nACGTACGT\n+\nIIIIHHHH\n"}
    resp = client.post("/api/jobs", json=payload, headers=bioops_headers)
    assert resp.status_code == 201
    job_id = resp.json()["id"]
    assert db.query(Job).count() == 1

    detail = client.get(f"/api/jobs/{job_id}", headers=bioops_headers).json()
    assert detail["status"] == "success"
    assert {s["status"] for s in detail["stages"]} == {"success"}


# ---------- API: sample path ----------

def test_api_rejects_empty_sample(client, bioops_headers, db, sample_ids):
    resp = client.post(
        "/api/jobs", json={"sampleId": sample_ids["blank"]}, headers=bioops_headers
    )
    assert resp.status_code == 400
    assert "空" in resp.json()["detail"]
    assert db.query(Job).count() == 0


def test_api_good_sample_starts_and_runs(client, bioops_headers, db, sample_ids):
    resp = client.post(
        "/api/jobs", json={"sampleId": sample_ids["good"]}, headers=bioops_headers
    )
    assert resp.status_code == 201
    job_id = resp.json()["id"]

    detail = client.get(f"/api/jobs/{job_id}", headers=bioops_headers).json()
    assert detail["status"] == "success"
    assert detail["sample_name"] == "test-good"


def test_samples_expose_has_content(client, bioops_headers, sample_ids):
    rows = client.get("/api/samples", headers=bioops_headers).json()
    by_id = {r["id"]: r for r in rows}
    assert by_id[sample_ids["good"]]["has_content"] is True
    assert by_id[sample_ids["blank"]]["has_content"] is False
