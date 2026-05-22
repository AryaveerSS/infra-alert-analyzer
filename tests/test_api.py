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
    data = response.json()
    assert "supported_alerts" in data

def test_crashloop_database():
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
    assert (
        "Escalate issue immediately to on-call team"
        in data["recommended_steps"]
    )

def test_crashloop_permission():
    payload = {
        "alert_type":
        "CrashLoopBackOff",
        "namespace":
        "prod",
        "pod_name":
        "backend",
        "logs":
        "Permission denied",
        "severity":
        "warning"
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
        "Permission issue accessing resources"
    )

def test_oom_java_heap():
    payload = {
        "alert_type":
        "OOMKilled",
        "namespace":
        "prod",
        "pod_name":
        "java-service",
        "logs":
        "Java heap exceeded",
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
        "Java heap memory exhaustion"
    )

def test_imagepull_auth():
    payload = {
        "alert_type":
        "ImagePullBackOff",
        "namespace":
        "prod",
        "pod_name":
        "backend",
        "logs":
        "Authentication failed",

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
        "Registry authentication failure"
    )


def test_unsupported_alert():

    payload = {

        "alert_type":
        "NodeFailure",

        "namespace":
        "prod",

        "pod_name":
        "backend",

        "logs":
        "Node unavailable",

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