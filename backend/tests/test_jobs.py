def test_get_jobs(client):
    response = client.post(
        "/jobs",
        json={
            "title": "Test Developer",
            "company": "Test Company",
            "location": "Test Location",
            "remote": True,
            "description": "Test job",
            "url": "https://example.com/test"
        }
    )

    assert response.status_code == 201

    response = client.get("/jobs")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["status_code"] == 200
    assert body["message"] == "Jobs retrieved successfully"

    jobs = body["data"]

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Test Developer"


def test_create_job_validation(client):
    response = client.post(
        "/jobs",
        json={
            "title": "Test Developer",
            "company": "Test Company",
            "location": "Tel Aviv",
            "remote": "not-a-boolean",
            "description": "Test job",
            "url": "https://example.com/test"
        }
    )

    assert response.status_code == 422

    assert response.json() == {
        "success": False,
        "status_code": 422,
        "message": "Invalid request data",
        "data": None
    }


def test_get_job_by_id_not_found(client):
    response = client.get("/jobs/999")

    assert response.status_code == 404

    assert response.json() == {
        "success": False,
        "status_code": 404,
        "message": "Job not found",
        "data": None
    }