from fastapi import HTTPException

from app.controller.helper_func.severity_check import get_severity_steps


from app.controller.helper_func.logs_check import  analyze_crashloop_logs,analyze_imagepull_logs, analyze_oom_logs

from app.core.logger import logger


def analyze_alert(alert):
    logger.info(
        f"Received alert "
        f"{alert.alert_type} "
        f"for pod "
        f"{alert.pod_name}"
    )
    alert_type = alert.alert_type.lower()
    severity_steps = get_severity_steps(alert.severity)
    if alert_type == "crashloopbackoff":
        cause, log_steps = (
            analyze_crashloop_logs(alert.logs)
        )
        summary = (
            "Pod is repeatedly crashing "
            "during startup."
        )
        commands = [
            f"kubectl logs "
            f"{alert.pod_name} "
            f"-n {alert.namespace}",

            f"kubectl describe pod "
            f"{alert.pod_name} "
            f"-n {alert.namespace}"
        ]
    elif alert_type == "oomkilled":
        cause, log_steps = (
            analyze_oom_logs(alert.logs)
        )
        summary = (
            "Container terminated "
            "due to memory limit exceeded."
        )
        commands = [
            f"kubectl top pod "
            f"{alert.pod_name} "
            f"-n {alert.namespace}",

            f"kubectl describe pod "
            f"{alert.pod_name} "
            f"-n {alert.namespace}"
        ]
    elif alert_type == "imagepullbackoff":
        cause, log_steps = (
            analyze_imagepull_logs(alert.logs)
        )
        summary = (
            "Pod unable to pull "
            "container image."
        )
        commands = [
            f"kubectl describe pod "
            f"{alert.pod_name} "
            f"-n {alert.namespace}",

            f"kubectl get events "
            f"-n {alert.namespace}"
        ]

    else:
        logger.warning(
            f"Unsupported alert type "
            f"{alert.alert_type}"
        )
        raise HTTPException(
            status_code=400,
            detail="Unsupported alert type"
        )
    logger.info(
        f"Successfully analyzed "
        f"{alert.alert_type}"
    )
    return {
        "summary":
        summary,

        "probable_cause":
        cause,

        "recommended_steps":
        log_steps + severity_steps,

        "commands":
        commands
    }