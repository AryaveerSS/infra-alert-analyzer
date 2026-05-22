from pydantic import BaseModel, Field
from typing import List


class AlertRequest(BaseModel):
    alert_type: str = Field(..., example="CrashLoopBackOff")
    namespace: str = Field(..., example="aml")
    pod_name: str = Field(..., example="nifi-0")
    logs: str = Field(..., example="Error: Unable to connect to database")
    severity: str = Field(..., example="critical")


class AlertResponse(BaseModel):
    summary: str
    probable_cause: str
    recommended_steps: List[str]
    commands: List[str]