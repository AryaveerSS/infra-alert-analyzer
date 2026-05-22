from fastapi import APIRouter
from app.schema.alert_models import AlertRequest,AlertResponse
from app.controller.analyzer import analyze_alert

router = APIRouter()

@router.post("/analyze",response_model=AlertResponse)
def analyze(alert: AlertRequest):
    return analyze_alert(alert)

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.get("/supported-alerts")
def supported_alerts():
    return {
        "supported_alerts": [
            "CrashLoopBackOff",
            "OOMKilled"
        ]
    }