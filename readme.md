# Infrastructure Alert Analyzer

A lightweight FastAPI backend service that analyzes infrastructure alerts and provides troubleshooting recommendations for Kubernetes workloads.

---

## Features

- REST API built with FastAPI
- Infrastructure alert analysis
- Rule-based troubleshooting engine
- Input validation using Pydantic
- Structured JSON responses
- Logging support
- Unit tests using Pytest
- Docker support
- Dynamic Kubernetes troubleshooting commands

---

## Supported Alert Types

### CrashLoopBackOff
Detects pod startup failures.

Example causes:
- Database connectivity issues
- Permission problems
- Port conflicts

### OOMKilled
Detects container memory-related failures.

Example causes:
- Memory exhaustion
- Java heap issues

### ImagePullBackOff
Detects container image pull failures.

Example causes:
- Registry authentication failure
- Missing image tags
- Registry connectivity issues

---

## Project Structure

```bash
infra-alert-analyzer/

├── app/
│   ├── api/
│   ├── controller/
│   │   └── helper_func/
│   ├── core/
│   ├── schema/
│   ├── services/
│   └── main.py
│
├── tests/
├── Dockerfile
├── requirements.txt
├── README.md
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>

cd infra-alert-analyzer
```

### 2. Create Virtual Environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac:

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
uvicorn app.main:app --reload
```

Application runs at:

```
http://127.0.0.1:8000
```

Swagger API docs:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Analyze Infrastructure Alert

```
POST /analyze
```

Request:

```json
{
  "alert_type": "CrashLoopBackOff",
  "namespace": "aml",
  "pod_name": "nifi-0",
  "logs": "Unable to connect to database",
  "severity": "critical"
}
```

Response:

```json
{
  "summary": "Pod is repeatedly crashing during startup.",
  "probable_cause": "Application unable to connect to database",
  "recommended_steps": [
    "Verify database connectivity",
    "Check environment variables",
    "Inspect secrets/configmaps"
  ],
  "commands": [
    "kubectl logs nifi-0 -n aml",
    "kubectl describe pod nifi-0 -n aml"
  ]
}
```

---

### Health Check

```
GET /health
```

Response:

```json
{
 "status":"healthy"
}
```

---

### Supported Alerts

```
GET /supported-alerts
```

Response:

```json
{
 "supported_alerts":[
  "CrashLoopBackOff",
  "OOMKilled",
  "ImagePullBackOff"
 ]
}
```

---

## Running Unit Tests

Run tests:

```bash
pytest
```

Expected:

```bash
6 passed
```

---

## Docker Support

Build image:

```bash
docker build -t infra-alert-analyzer .
```

Run container:

```bash
docker run -p 8000:8000 infra-alert-analyzer
```

---

## Logging

Application logs:

- Incoming alerts
- Successful alert analysis
- Unsupported alert types

Example:

```text
INFO - Received alert CrashLoopBackOff for pod nifi-0

INFO - Successfully analyzed CrashLoopBackOff

WARNING - Unsupported alert type NodeFailure
```

---

## Approach

The application uses a rule-based alert analysis engine.

Analysis depends on:

- Alert Type
- Log Patterns
- Severity Level

Helper functions separate severity handling and log analysis logic to keep the service layer clean and maintainable.

---

## Future Improvements

- Kubernetes deployment YAML
- Persistent alert storage
- AI-based root cause analysis
- Alert history dashboard

---

Developed using FastAPI + Python