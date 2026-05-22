from pydantic import BaseModel, Field
from typing import List


class AlertRequest(BaseModel):
    alert_type:str = Field(...,json_schema_extra={"example": "CrashLoopBackOff"}
    )

    namespace:str = Field(...,json_schema_extra={"example": "aml"})

    pod_name:str = Field(...,json_schema_extra={"example": "nifi-0"})

    logs:str = Field(...,json_schema_extra={"example":"Error: Unable to connect to database"})

    severity: str = Field(...,json_schema_extra={"example": "critical"})


class AlertResponse(BaseModel):

    summary: str
    probable_cause: str
    recommended_steps: List[str]
    commands: List[str]