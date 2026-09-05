from app.core import SuccessMessage, StatusCode

def test_health_check(client):
    response = client.get("/")

    assert response.status_code == StatusCode.OK

    assert response.json() == {
        "success": True,
        "status_code": StatusCode.OK,
        "message": SuccessMessage.SUCCESS,
        "data": None
    }