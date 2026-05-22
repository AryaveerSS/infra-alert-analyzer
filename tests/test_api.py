from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }

def test_supported_alerts():
    response = client.get(
        "/supported-alerts"
    )
    assert response.status_code == 200

def test_crashloopbackoff():
    payload = {
        "alert_type":
        "CrashLoopBackOff",
        "namespace":
        "aml",
        "pod_name":
        "nifi-0",
        "logs":
        "Unable to connect to database",
        "severity":
        "critical"
    }
    response = client.post(
        "/analyze",
        json=payload
    )
    data = response.json()
    assert response.status_code == 200
    assert (
        data["probable_cause"]
        ==
        "Application unable to connect to database"
    )

def test_oomkilled():
    payload = {
        "alert_type":
        "OOMKilled",
        "namespace":
        "prod",
        "pod_name":
        "backend-1",
        "logs":
        "Memory exceeded",
        "severity":
        "critical"
    }
    response = client.post(
        "/analyze",
        json=payload
    )
    data = response.json()
    assert response.status_code == 200
    assert (
        data["probable_cause"]
        ==
        "Application exceeded allocated memory."
    )
def test_imagepullbackoff():
    payload = {
        "alert_type":
        "ImagePullBackOff",
        "namespace":
        "prod",
        "pod_name":
        "api-server",
        "logs":
        "Image not found",
        "severity":
        "warning"
    }
    response = client.post(
        "/analyze",
        json=payload
    )
    assert response.status_code == 200


def test_unsupported_alert():
    payload = {
        "alert_type":
        "UnknownAlert",
        "namespace":
        "aml",
        "pod_name":
        "test",
        "logs":
        "error",
        "severity":
        "critical"
    }
    response = client.post(
        "/analyze",
        json=payload
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail":
        "Unsupported alert type"
    }