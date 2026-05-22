def analyze_crashloop_logs(logs):
    logs = logs.lower()
    if "database" in logs:
        return (
            "Application unable to connect to database",
            [
                "Verify database connectivity",
                "Check environment variables",
                "Inspect secrets/configmaps"
            ]
        )
    elif "permission" in logs:
        return (
            "Permission issue accessing resources",
            [
                "Check RBAC permissions",
                "Inspect file permissions",
                "Verify service account configuration"
            ]
        )
    elif "port" in logs:
        return (
            "Port conflict during startup",
            [
                "Verify container ports",
                "Inspect deployment manifest",
                "Check conflicting services"
            ]
        )
    return (
        "Application startup failure",
        [
            "Inspect startup commands",
            "Review container configuration"
        ]
    )

def analyze_oom_logs(logs):
    logs = logs.lower()
    if "java heap" in logs:
        return (
            "Java heap memory exhaustion",
            [
                "Adjust JVM heap settings"
            ]
        )
    return (
        "Application exceeded allocated memory",
        [
            "Check memory usage",
            "Inspect memory leaks",
            "Increase memory limits"
        ]
    )

def analyze_imagepull_logs(logs):
    logs = logs.lower()
    if "authentication" in logs:
        return (
            "Registry authentication failure",
            [
                "Verify image pull secrets"
            ]
        )
    elif "not found" in logs:
        return (
            "Container image not found",
            [
                "Verify image tag"
            ]
        )
    return (
        "Image registry access issue",
        [
            "Verify image name",
            "Check registry connectivity"
        ]
    )
