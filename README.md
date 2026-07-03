# Smart Education Analytics and Student Performance Prediction

This project solves **Case Study 8: Smart Education Analytics and Student Performance Prediction System using Apache Spark**.

The main solution is implemented and executed in:

`notebooks/smart_education_analytics_q1_q7.ipynb`

It covers Q1 to Q7:

1. Spark initialization and data loading
2. RDD transformations and actions
3. Key-value RDD operations and persistence
4. Spark DataFrame joins and aggregation
5. EDA and Spark SQL queries
6. ETL pipeline development
7. Spark ML model for student performance prediction

Additional submission artifacts are also included:

- Dockerfile
- Kubernetes deployment and service YAML files
- GitHub Actions CI workflow
- Project documentation
- Output files and model metrics

## Project Structure

```text
case_study/
|-- data/
|   |-- README.md
|   |-- assessments.csv              # local only, ignored by Git
|   |-- courses.csv                  # local only, ignored by Git
|   |-- studentAssessment.csv        # local only, ignored by Git
|   |-- studentInfo.csv              # local only, ignored by Git
|   |-- studentRegistration.csv      # local only, ignored by Git
|   |-- studentVle.csv               # local only, ignored by Git
|   |-- vle.csv                      # local only, ignored by Git
|-- docs/
|   |-- Case Study8.pdf
|   |-- PROJECT_DOCUMENTATION.md
|-- notebooks/
|   |-- smart_education_analytics_q1_q7.ipynb
|-- outputs/
|   |-- student_features.csv
|   |-- model_metrics.json
|   |-- sample_predictions.csv
|-- src/
|   |-- run_notebook.py
|   |-- health_check.py
|-- k8s/
|   |-- deployment.yaml
|   |-- service.yaml
|-- .github/
|   |-- workflows/
|   |   |-- ci.yml
|-- Dockerfile
|-- requirements.txt
|-- README.md
```

## Dataset Notes

The provided data matches the Open University Learning Analytics Dataset (OULAD), with course, student, assessment, registration, and VLE activity tables.

Dataset source link:

```text
https://figshare.com/articles/dataset/OULAD_Open_University_Learning_Analytics_Dataset/5081998?file=8606371
```

Dataset CSV files are intentionally ignored by Git because they are local input data and `studentVle.csv` is too large for normal GitHub upload. Keep the CSV files in `data/` when running locally.

The case-study prompt mentions attendance and placement data, but no separate attendance or placement files were provided. Therefore:

- `studentVle.csv` clicks are used as an online attendance or engagement proxy.
- `final_result` is used as the available outcome proxy for student success prediction.

## Setup

Use Python 3.10 for best PySpark compatibility on this Windows setup.

```powershell
cd C:\Users\15dha\OneDrive\Desktop\case_study

python -m venv .venv310
.\.venv310\Scripts\activate
python -m pip install -r requirements.txt
```

If using the existing environment:

```powershell
cd C:\Users\15dha\OneDrive\Desktop\case_study

$env:PYSPARK_PYTHON=(Resolve-Path ".\.venv310\Scripts\python.exe").Path
$env:PYSPARK_DRIVER_PYTHON=$env:PYSPARK_PYTHON
```

## Run Notebook

Open the notebook:

```powershell
.\.venv310\Scripts\python -m jupyter notebook notebooks\smart_education_analytics_q1_q7.ipynb
```

Or execute it from the command line:

```powershell
.\.venv310\Scripts\python src\run_notebook.py
```

## Output Summary

The notebook creates these key outputs:

- `outputs/student_features.csv`
- `outputs/model_metrics.json`
- `outputs/sample_predictions.csv`

Final model metrics:

| Metric | Value |
|---|---:|
| AUC | 0.9706 |
| Accuracy | 0.9142 |
| F1 Score | 0.9142 |

## Docker

Build the image:

```powershell
docker build -t smart-education-analytics:latest .
```

Run the container:

```powershell
docker run --rm -v ${PWD}\data:/app/data -v ${PWD}\outputs:/app/outputs smart-education-analytics:latest
```

The Docker image runs the notebook through `src/run_notebook.py`.
During local Docker builds, the local `data/*.csv` files are copied into the image. They are still ignored by Git and are not uploaded to GitHub.

## Kubernetes

For this local Docker Desktop Kubernetes setup, build the image and tag it for Kubernetes:

```powershell
docker build -t smart-education-analytics:latest -t smart-education-analytics:k8s-final-v2 .
```

The Kubernetes deployment runs `src/health_check.py` and then serves the generated files from `outputs/` on port `8080`. The full Spark notebook execution is handled by the notebook runner and Docker run command, not during every pod startup.

Apply manifests:

```powershell
kubectl apply -f k8s\deployment.yaml
kubectl apply -f k8s\service.yaml
```

Check deployment:

```powershell
kubectl get pods
kubectl get svc
kubectl logs deployment/smart-education-analytics
```

Expected successful log output includes:

```text
Project structure check passed.
Serving HTTP on 0.0.0.0 port 8080
```

## CI/CD

The workflow is located at:

`.github/workflows/ci.yml`

It checks:

- Python dependency installation
- Project structure
- Required files
- Notebook availability
- Output metrics file format

## Documentation

Detailed documentation is available here:

`docs/PROJECT_DOCUMENTATION.md`

It explains the data loading, operations, outputs, challenges, solutions, and complete code flow.

## Final Submission Status

The notebook, documentation, Docker setup, Kubernetes manifests, GitHub Actions workflow, generated outputs, and local Kubernetes deployment are ready. If your evaluator specifically requires image evidence, keep the Docker, Kubernetes, and GitHub Actions screenshots inside the matching folders under `screenshots/`.
