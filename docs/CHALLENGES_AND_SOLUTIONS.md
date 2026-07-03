# Challenges and Solutions

Project: Case Study 8 - Smart Education Analytics and Student Performance Prediction System using Apache Spark

This file explains the main problems faced during project execution, how each one was solved, how to explain it in an interview or viva, and what would be a better way to handle it in a cleaner production workflow.

## 1. Dataset Size and GitHub Upload Limit

### What happened

The project uses OULAD CSV files, and `studentVle.csv` is very large. Uploading all CSV files directly to GitHub or inside the final zip would make the repository/package too large.

### Why it happened

GitHub and assignment upload systems are not good places for large raw datasets. The question also allows datasets or dataset links.

### How it was solved

- Raw CSV files were kept locally in `data/`.
- `data/*.csv` was added to `.gitignore`.
- `data/README.md` was kept in Git to list required dataset files.
- The Figshare OULAD dataset link was added to documentation.

Dataset link:

```text
https://figshare.com/articles/dataset/OULAD_Open_University_Learning_Analytics_Dataset/5081998?file=8606371
```

### Self explanation

I did not upload raw data because one CSV file is too large. Instead, I documented the dataset source and kept the project reproducible by explaining which files should be placed in `data/`.

### Better way

For a production project, use cloud storage such as S3, Azure Blob, Google Cloud Storage, or DVC, then store only dataset links and data-loading instructions in Git.

## 2. Two Virtual Environments

### What happened

Two virtual environments existed during setup: `.venv` and `.venv310`.

### Why it happened

PySpark compatibility was better with Python 3.10. Python 3.12 created compatibility problems during execution.

### How it was solved

- `.venv310` became the final working environment.
- Virtual environments were ignored by Git.
- Later, Docker became the more reliable execution environment for validation.

### Self explanation

The first environment was not the final stable one. I used Python 3.10 because PySpark worked more reliably with it.

### Better way

Start with a fixed project environment from the beginning:

```powershell
python -m venv .venv310
.\.venv310\Scripts\activate
python -m pip install -r requirements.txt
```

Also mention the required Python version clearly in `README.md`.

## 3. PySpark Python Path Issue on Windows

### What happened

Spark workers tried to use `python3`, but Windows could not find it.

### Error symptom

```text
Python was not found; run without arguments to install from the Microsoft Store
```

### Why it happened

On Windows, `python3` is often not available as a command. Spark worker processes need to know which Python executable to use.

### How it was solved

The PySpark Python environment variables were set:

```powershell
$env:PYSPARK_PYTHON=(Resolve-Path ".\.venv310\Scripts\python.exe").Path
$env:PYSPARK_DRIVER_PYTHON=$env:PYSPARK_PYTHON
```

### Self explanation

Spark runs Python code in worker processes. I had to tell Spark exactly which Python executable to use on Windows.

### Better way

Use Docker for consistent execution, or create a startup script that sets these variables automatically.

## 4. Windows Hadoop / Parquet Save Issue

### What happened

Saving Spark outputs as Parquet or saving Spark model directories caused Hadoop-related errors on Windows.

### Error symptom

```text
HADOOP_HOME and hadoop.home.dir are unset
```

### Why it happened

Spark uses Hadoop file-system APIs. On Windows, some write operations can require Hadoop binaries such as `winutils.exe`.

### How it was solved

- Final ETL output was saved as CSV.
- Model metrics were saved as JSON.
- Sample predictions were saved as CSV.
- The Spark ML model was trained and evaluated in memory.

### Self explanation

Instead of making the project depend on extra Hadoop Windows binaries, I saved the required assignment outputs in portable formats: CSV and JSON.

### Better way

For production, run Spark on Linux, Docker, Databricks, EMR, or a real Spark cluster where Hadoop support is already configured.

## 5. Docker Build Problem

### What happened

The first Docker build took a long time and package installation caused issues.

### Why it happened

The Docker image needed Java for Spark. PySpark requires a JVM, so the image had to install OpenJDK.

### How it was solved

The Dockerfile used:

```dockerfile
FROM python:3.10-slim-bookworm
```

and installed:

```dockerfile
openjdk-17-jre-headless
```

### Self explanation

PySpark is Python code, but Spark itself runs on the JVM. That is why Java was needed inside the Docker image.

### Better way

Use a Spark-ready base image if available, or keep a Docker cache so repeated builds are faster.

## 6. Docker Run Before Docker Build

### What happened

`docker run` was executed before the local image existed.

### Error symptom

```text
Unable to find image 'smart-education-analytics:latest' locally
pull access denied
```

### Why it happened

Docker first checks local images. If the image is not present, it tries to pull from Docker Hub. Since this image was only local, Docker Hub did not have it.

### How it was solved

The image was built first:

```powershell
docker build -t smart-education-analytics:latest .
```

Then it was run:

```powershell
docker run --rm -v ${PWD}\data:/app/data -v ${PWD}\outputs:/app/outputs smart-education-analytics:latest
```

### Self explanation

Docker cannot run an image before it is built locally or pulled from a registry.

### Better way

Always follow this order:

1. Build image.
2. Verify image exists.
3. Run image.

```powershell
docker images smart-education-analytics
```

## 7. Kubernetes Context Not Ready

### What happened

`kubectl config use-context docker-desktop` failed at first.

### Error symptom

```text
error: no context exists with the name: "docker-desktop"
```

### Why it happened

Docker Desktop Kubernetes was enabled but had not finished starting. The context was not created yet.

### How it was solved

Waited until Docker Desktop showed Kubernetes as running, then checked:

```powershell
kubectl config get-contexts
kubectl config use-context docker-desktop
kubectl cluster-info
```

### Self explanation

The Kubernetes command failed because the cluster was not fully ready, not because the YAML files were wrong.

### Better way

Check cluster readiness before applying YAML:

```powershell
kubectl config get-contexts
kubectl cluster-info
kubectl get nodes
```

## 8. Kubernetes HostPath Mount Failed

### What happened

Kubernetes could not mount the local Windows `data/` folder.

### Error symptom

```text
hostPath type check failed: .../case_study/data is not a directory
```

### Why it happened

Docker Desktop Kubernetes runs inside a Linux environment. Windows paths do not always map cleanly as Kubernetes `hostPath` volumes.

### How it was solved

For local Kubernetes demonstration:

- The Docker image was built with local `data/` copied into `/app/data`.
- Raw CSV files stayed ignored by Git.
- Kubernetes used the image content instead of a Windows hostPath mount.

### Self explanation

The problem was not the data itself. It was the Windows-to-Linux path mapping for Kubernetes volumes.

### Better way

Use one of these:

- A Kubernetes `PersistentVolume` configured correctly for the cluster.
- A cloud object storage bucket.
- A container image only for local demo.
- A mounted ConfigMap/Secret only for small config files, not large datasets.

## 9. Kubernetes Used a Cached Image

### What happened

Even after rebuilding Docker, Kubernetes still ran an older image.

### Error symptom

```text
FileNotFoundError: data/ folder not found
```

### Why it happened

The deployment used the `latest` tag. Kubernetes can reuse a cached image with the same tag.

### How it was solved

A new tag was used:

```text
smart-education-analytics:k8s-final-v2
```

### Self explanation

Using a fresh image tag forced Kubernetes to use the corrected image instead of a cached old one.

### Better way

Avoid `latest` for deployments. Use versioned tags:

```text
smart-education-analytics:v1
smart-education-analytics:v2
smart-education-analytics:2026-07-03
```

## 10. Running Full Notebook During Pod Startup Was Heavy

### What happened

The first Kubernetes command ran the full notebook before starting the HTTP server.

### Why it was a problem

The pod stayed busy running Spark. A deployment should start quickly and expose a stable service.

### How it was solved

The Kubernetes command was changed from:

```text
python src/run_notebook.py && python -m http.server 8080 --directory outputs
```

to:

```text
python src/health_check.py && python -m http.server 8080 --directory outputs
```

### Self explanation

Notebook execution is a batch job. Kubernetes deployment should serve the generated outputs and validate that required files exist.

### Better way

Separate the system into two workloads:

- Batch job: run Spark notebook or ETL.
- Service deployment: serve outputs or model API.

## 11. Git Accidentally Tracked Dataset Files

### What happened

At one point, dataset files were tracked by Git.

### Why it happened

The data files existed before the final `.gitignore` cleanup.

### How it was solved

The data files were removed from Git tracking while kept locally:

```powershell
git rm --cached data/*.csv
```

Then `.gitignore` was used:

```text
data/*.csv
!data/README.md
```

### Self explanation

I did not delete the local datasets. I only removed them from Git tracking.

### Better way

Create `.gitignore` before the first commit and check tracked files:

```powershell
git ls-files data
```

Expected:

```text
data/README.md
```

## Final Lesson

The main improvement for future projects is to define the execution flow first:

1. Prepare folder structure.
2. Add `.gitignore`.
3. Add dataset README/link.
4. Build notebook and outputs.
5. Add Docker.
6. Add Kubernetes.
7. Add CI/CD.
8. Add screenshots.
9. Create final zip.

