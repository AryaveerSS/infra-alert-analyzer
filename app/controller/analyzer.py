from fastapi import HTTPException
from app.controller.helper_func.severity_check import get_severity_steps
from app.controller.helper_func.logs_check import analyze_crashloop_logs,analyze_imagepull_logs,analyze_oom_logs

def analyze_alert(alert):
    alert_type = alert.alert_type.lower()
    severity_steps = get_severity_steps(
        alert.severity
    )
    if alert_type == "crashloopbackoff":
        cause, log_steps = analyze_crashloop_logs(
            alert.logs
        )
        return {
            "summary":
            "Pod is repeatedly crashing during startup.",
            "probable_cause":
            cause,
            "recommended_steps":
            log_steps + severity_steps,
            "commands": [
                f"kubectl logs {alert.pod_name} -n {alert.namespace}",
                f"kubectl describe pod {alert.pod_name} -n {alert.namespace}"
            ]
        }
    elif alert_type == "oomkilled":
        cause, log_steps = analyze_oom_logs(
            alert.logs
        )
        return {
            "summary":
            "Container terminated due to memory limit exceeded.",
            "probable_cause":
            cause,
            "recommended_steps":
            log_steps + severity_steps,
            "commands": [
                f"kubectl top pod {alert.pod_name} -n {alert.namespace}",
                f"kubectl describe pod {alert.pod_name} -n {alert.namespace}"
            ]
        }
    elif alert_type == "imagepullbackoff":
        cause, log_steps = analyze_imagepull_logs(
            alert.logs
        )
        return {
            "summary":
            "Pod unable to pull container image.",
            "probable_cause":
            cause,
            "recommended_steps":
            log_steps + severity_steps,
            "commands": [
                f"kubectl describe pod {alert.pod_name} -n {alert.namespace}",
                f"kubectl get events -n {alert.namespace}"
            ]
        }
    raise HTTPException(
        status_code=400,
        detail="Unsupported alert type"
    )