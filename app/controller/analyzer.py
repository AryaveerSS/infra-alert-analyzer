from fastapi import HTTPException
from app.schema.alert_models import AlertRequest,AlertResponse

def analyze_alert(alert:AlertRequest):
    alert_type = alert.alert_type.lower()
    if alert_type == "crashloopbackoff":
        cause = "Application startup failure"
        if "database" in alert.logs.lower():
            cause = "Application unable to connect to database"
        return {
            "summary": "Pod is repeatedly crashing during startup.",
            "probable_cause": cause,
            "recommended_steps": [
                "Verify database connectivity",
                "Check environment variables",
                "Inspect secrets/configmaps"
            ],

            "commands": [
                f"kubectl logs {alert.pod_name} -n {alert.namespace}",
                f"kubectl describe pod {alert.pod_name} -n {alert.namespace}"
            ]
        }

    elif alert_type == "oomkilled":
        return {
            "summary": "Container terminated because memory limit exceeded.",
            "probable_cause":
            "Application exceeded allocated memory.",

            "recommended_steps": [
                "Increase memory limits",
                "Check application memory usage",
                "Inspect possible memory leaks"
            ],
            "commands": [
                f"kubectl top pod {alert.pod_name} -n {alert.namespace}",
                f"kubectl describe pod {alert.pod_name} -n {alert.namespace}"
            ]
        }
    elif alert_type == "imagepullbackoff":
        return {
        "summary":
        "Pod unable to pull container image.",
        "probable_cause":
        "Container image missing, incorrect image name, or registry access issue.",

        "recommended_steps": [
            "Verify image name and tag",
            "Check registry connectivity",
            "Confirm image exists in registry",
            "Inspect image pull secrets"
        ],

        "commands": [
            f"kubectl describe pod {alert.pod_name} -n {alert.namespace}",
            f"kubectl get events -n {alert.namespace}"
        ]
    }

    raise HTTPException(
        status_code=400,
        detail="Unsupported alert type"
    )