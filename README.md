# devops-k8s-cicd

A production-style application stack built with **Flask + PostgreSQL**, deployed on **Kubernetes (Minikube)**, with a fully automated **Jenkins CI/CD pipeline**.

Built as part of a DevOps Infrastructure Challenge — focusing on containerization, deployment automation, observability, and operational debugging.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask |
| Database | PostgreSQL 15 |
| Container | Docker |
| Orchestration | Kubernetes (Minikube) |
| CI/CD | Jenkins |
| Registry | DockerHub |

---

## Project Structure

```
devops-k8s-cicd/
├── app/
│   ├── app.py                  # Flask API
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Container definition
├── k8s/
│   ├── namespace.yaml
│   ├── secret.yaml             # DB credentials (base64)
│   ├── postgres-deployment.yaml
│   ├── flask-deployment.yaml   # Includes readiness/liveness probes
│   └── services.yaml
└── Jenkins/
    └── Jenkinsfile          # CI/CD pipeline
```

---

## Features

### Working Kubernetes Deployment
- Flask API + PostgreSQL running end-to-end on Minikube
- Credentials managed via Kubernetes Secrets (never hardcoded)
- Resource requests and limits set on all containers

### CI/CD Pipeline (Jenkins)
- Triggers on every push to `main`
- Builds Docker image and pushes to DockerHub (tagged with Git SHA)
- Applies Kubernetes manifests and verifies rollout status

### Reliability Feature — Readiness & Liveness Probes
- **Readiness probe** (`/ready`): checks actual database connectivity before accepting traffic
- **Liveness probe** (`/health`): restarts the pod if the Flask process becomes unresponsive
- Prevents users from ever hitting a broken pod during startup or DB outages

### Failure Simulation & Debugging
- Intentionally injected a wrong database password via `kubectl set env`
- Debugged using: pod events → logs → exec into pod → env inspection → root cause → fix
- Demonstrates how probes protect traffic during failures

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

### 1. Start Minikube

```bash
minikube start --driver=docker
```

### 2. Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/services.yaml
kubectl apply -f k8s/flask-deployment.yaml
```

### 3. Check Pods Are Running

```bash
kubectl get pods -n myapp
```

All pods should show `Running` and `1/1 READY`.

### 4. Access the App

```bash
minikube service flask-svc -n myapp --url
```

Open the URL in your browser — you should see:

```json
{ "message": "Flask + PostgreSQL on Kubernetes!" }
```

---

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /` | Main response |
| `GET /health` | Liveness probe — checks Flask process |
| `GET /ready` | Readiness probe — checks DB connectivity |

---

## CI/CD Setup

Add these secrets to your GitHub repository (`Settings → Secrets → Actions`):

| Secret | Value |
|--------|-------|
| `DOCKER_USERNAME` | Your DockerHub username |
| `DOCKER_PASSWORD` | Your DockerHub password or access token |
| `KUBECONFIG` | Contents of `~/.kube/config` from your local machine |

Push to `main` to trigger the pipeline automatically.

---

## Debugging the Failure Scenario

To reproduce the intentional failure:

```bash
# Inject wrong password
kubectl set env deployment/flask-api DB_PASS="WRONGPASSWORD" -n myapp

# Observe pods go to 0/1 READY
kubectl get pods -n myapp

# Check events
kubectl describe pod -l app=flask-api -n myapp

# Check logs
kubectl logs -l app=flask-api -n myapp

# Inspect env vars on the pod
kubectl exec -it <pod-name> -n myapp -- env | grep DB_

# Fix it
kubectl set env deployment/flask-api DB_PASS="apppassword" -n myapp
```

---

## Tradeoffs & Production Improvements

| What's simplified | What would change in production |
|-------------------|---------------------------------|
| No persistent volume for Postgres | Add `PersistentVolumeClaim` — data currently resets on pod restart |
| Single Postgres pod | Use a managed DB (AWS RDS, Cloud SQL) or StatefulSet with replicas |
| NodePort service | Replace with Ingress + TLS termination |
| No autoscaling | Add `HorizontalPodAutoscaler` for Flask based on CPU/RPS |
| No centralized logging | Add Loki + Grafana or ship logs to a log aggregator |

---

## License

MIT
