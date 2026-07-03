# Command Execution Flow

This file lists the important commands used in the project, which ones were wrong or risky, the correct command flow, and how to check success after each step.

## A. Commands That Were Wrong, Risky, or Out of Order

| Command or action | Problem | Correct action |
|---|---|---|
| `git add.` | Wrong syntax. Git command needs a space. | Use `git add .` or stage exact files. |
| `git add` with no path | Nothing gets staged. | Use `git add README.md` or `git add .`. |
| Running `docker run smart-education-analytics:latest` before `docker build` | Image did not exist locally, so Docker tried to pull it from Docker Hub. | Build first with `docker build -t smart-education-analytics:latest .`. |
| Adding dataset CSV files to Git | Large dataset files should not be uploaded directly. | Use `.gitignore`, keep `data/README.md`, and add dataset link. |
| Reusing `latest` for Kubernetes after rebuilding | Kubernetes reused cached image content. | Use a fresh tag such as `smart-education-analytics:k8s-final-v2`. |
| `kubectl config use-context docker-desktop` before Kubernetes was ready | Context did not exist yet. | Wait for Docker Desktop Kubernetes to show Running, then check contexts. |
| `kubectl logs <pod>` while pod was `ContainerCreating` | Logs are unavailable until container starts. | Use `kubectl describe pod <pod>` to inspect mount/image errors. |
| Windows `hostPath` mount for `data/` | Docker Desktop Kubernetes did not recognize the Windows path as a Linux directory. | Copy local data into the local Docker image for demo, or use a real persistent volume. |
| Pasting logs together with commands | Creates confusing terminal input and can run wrong text. | Paste one clean command at a time. |

## B. Correct Full Project Command Flow

Run these commands from:

```powershell
cd "C:\Users\15dha\OneDrive\Desktop\case_study"
```

### 1. Check Project Structure

```powershell
dir
```

### Use

Confirms that required folders exist: `data`, `docs`, `notebooks`, `outputs`, `src`, `k8s`, `screenshots`.

### Success criteria

You should see files/folders like:

```text
README.md
Dockerfile
requirements.txt
data
notebooks
outputs
k8s
src
```

## 2. Check Git Status

```powershell
git status --short --branch
```

### Use

Shows current branch and changed files.

### Success criteria

Clean state looks like:

```text
## main...origin/main
```

If changed files appear, decide whether to commit them or ignore them.

## 3. Confirm Dataset Files Are Not Tracked by Git

```powershell
git ls-files data
```

### Use

Checks which `data/` files are tracked by Git.

### Success criteria

Expected output:

```text
data/README.md
```

Raw CSV files should not appear.

## 4. Check Dataset Ignore Rules

```powershell
git check-ignore -v --no-index data\studentVle.csv data\assessments.csv data\README.md
```

### Use

Confirms that CSV files are ignored and `data/README.md` is allowed.

### Success criteria

Expected meaning:

- `data/*.csv` ignores CSV files.
- `!data/README.md` keeps dataset instructions tracked.

## 5. Run Local Project Health Check

```powershell
python src\health_check.py
```

### Use

Checks required files and model metrics.

### Success criteria

Expected output includes:

```text
Project structure check passed.
Model: Spark ML Logistic Regression
AUC: 0.9706097899274218
Accuracy: 0.9142137572800252
F1: 0.9142484488670111
```

## 6. Run Notebook from Command Line

```powershell
python src\run_notebook.py
```

### Use

Executes the notebook from top to bottom.

### Success criteria

Expected output:

```text
Executed code cells: 12
Notebook error outputs: 0
```

Generated files should exist:

```text
outputs/student_features.csv
outputs/model_metrics.json
outputs/sample_predictions.csv
```

## 7. Build Docker Image

```powershell
docker build -t smart-education-analytics:latest .
```

### Use

Builds the Docker image from `Dockerfile`.

### Success criteria

Expected ending:

```text
naming to docker.io/library/smart-education-analytics:latest done
```

Check image:

```powershell
docker images smart-education-analytics
```

## 8. Run Docker Container

```powershell
docker run --rm -v ${PWD}\data:/app/data -v ${PWD}\outputs:/app/outputs smart-education-analytics:latest
```

### Use

Runs the project inside Docker and writes outputs back to local `outputs/`.

### Success criteria

Container finishes without error, and outputs exist:

```powershell
dir outputs
```

## 9. Build Docker Image for Kubernetes

```powershell
docker build -t smart-education-analytics:latest -t smart-education-analytics:k8s-final-v2 .
```

### Use

Builds a tagged local image that Kubernetes can use without reusing old `latest`.

### Success criteria

Check:

```powershell
docker images smart-education-analytics
```

Expected tags:

```text
latest
k8s-final-v2
```

## 10. Enable and Check Kubernetes

```powershell
kubectl config get-contexts
kubectl config use-context docker-desktop
kubectl cluster-info
```

### Use

Confirms Docker Desktop Kubernetes is running.

### Success criteria

Expected:

```text
Switched to context "docker-desktop".
Kubernetes control plane is running
```

If context does not exist, wait until Docker Desktop Kubernetes shows Running.

## 11. Apply Kubernetes Manifests

```powershell
kubectl apply -f k8s\deployment.yaml
kubectl apply -f k8s\service.yaml
```

### Use

Creates or updates the Kubernetes deployment and service.

### Success criteria

Expected:

```text
deployment.apps/smart-education-analytics configured
service/smart-education-analytics configured
```

`created` or `unchanged` is also acceptable.

## 12. Verify Kubernetes Deployment

```powershell
kubectl get pods,svc,deployment -o wide
```

### Use

Checks pod, service, and deployment status.

### Success criteria

Expected:

```text
pod/... 1/1 Running
deployment.apps/smart-education-analytics 1/1
service/smart-education-analytics 8080/TCP
```

## 13. Check Kubernetes Logs

```powershell
kubectl logs deployment/smart-education-analytics --tail=20
```

### Use

Confirms the container passed health check and started the HTTP server.

### Success criteria

Expected:

```text
Project structure check passed.
Serving HTTP on 0.0.0.0 port 8080
```

## 14. Verify HTTP Output Inside Pod

```powershell
kubectl exec deployment/smart-education-analytics -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8080/model_metrics.json', timeout=5).read().decode()[:300])"
```

### Use

Confirms the server is actually serving output files.

### Success criteria

Expected output includes:

```json
"model": "Spark ML Logistic Regression"
"auc": 0.9706097899274218
```

## 15. Commit Project Changes

```powershell
git add README.md docs\PROJECT_DOCUMENTATION.md data\README.md
git commit -m "Add OULAD dataset source link"
git push origin main
```

### Use

Stages, commits, and pushes documentation changes.

### Success criteria

Expected push output:

```text
main -> main
```

Check:

```powershell
git status --short --branch
```

Expected:

```text
## main...origin/main
```

## 16. Create Final Submission Zip

```powershell
Compress-Archive -Path submit -DestinationPath submit.zip -Force
```

### Use

Creates zip file for assignment upload.

### Success criteria

Check file size:

```powershell
Get-Item submit.zip | Select-Object FullName,Length
```

Expected:

```text
submit.zip exists and is below 100 MB
```

## C. Best Clean Execution Order

Use this order next time:

1. Create folder structure.
2. Add `.gitignore`.
3. Add dataset README and dataset link.
4. Put CSV files locally in `data/`.
5. Build and run notebook.
6. Save outputs.
7. Add documentation.
8. Build Docker image.
9. Run Docker image.
10. Enable Kubernetes.
11. Apply Kubernetes YAML.
12. Verify pod/service/logs.
13. Add screenshots.
14. Push to GitHub.
15. Create final zip.

