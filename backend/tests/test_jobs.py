from app.models.job import Job
from app.core import SuccessMessage, ErrorMessage, StatusCode


def test_get_jobs(client, db):

    job = Job(
        airtable_id="test-job-1",
        title="Test Developer",
        company="Test Company",
        location=["Test Location"],
        remote=True,
        description="Test job",
        url="https://example.com/test",
    )

    db.add(job)
    db.commit()
    db.close()

    response = client.get("/jobs")

    assert response.status_code == StatusCode.OK

    body = response.json()

    assert body["success"] is True
    assert body["status_code"] == StatusCode.OK
    assert body["message"] == SuccessMessage.JOBS_RETRIEVED

    jobs = body["data"]

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Test Developer"


def test_get_job_by_id_not_found(client):
    response = client.get("/jobs/999")

    assert response.status_code == StatusCode.NOT_FOUND

    assert response.json() == {
        "success": False,
        "status_code": StatusCode.NOT_FOUND,
        "message": ErrorMessage.JOB_NOT_FOUND,
        "data": None,
    }
