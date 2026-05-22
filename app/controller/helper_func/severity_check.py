def get_severity_steps(severity):
    severity = severity.lower()
    if severity == "critical":
        return [
            "Escalate issue immediately to on-call team"
        ]
    elif severity == "warning":
        return [
            "Monitor issue before escalation"
        ]
    elif severity == "low":
        return [
            "Track issue during routine maintenance"
        ]
    return []