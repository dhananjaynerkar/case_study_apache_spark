# Smart Education Analytics Case Study Documentation

## Project Overview

This project solves **Case Study 8: Smart Education Analytics and Student Performance Prediction System using Apache Spark** up to **Question 7** in one executed Jupyter notebook:

`notebooks/smart_education_analytics_q1_q7.ipynb`

The solution uses PySpark to load education datasets, perform RDD operations, key-value operations, DataFrame joins, Spark SQL analysis, ETL feature engineering, and a Spark ML model for student performance prediction.

The original case-study PDF asks for attendance and placement analysis, but the provided files do not contain separate attendance or placement datasets. Because of this:

- `studentVle.csv` click activity is used as an online attendance or engagement proxy.
- `final_result` is used as the available academic outcome proxy instead of placement status.

## Final File Structure

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
|   |-- matplotlib_cache/
|   |-- ipython/
|   |-- student_features_parquet/
|-- src/
|   |-- run_notebook.py
|   |-- health_check.py
|-- k8s/
|   |-- deployment.yaml
|   |-- service.yaml
|-- screenshots/
|   |-- docker/
|   |-- github_actions/
|   |-- kubernetes/
|-- .github/
|   |-- workflows/
|   |   |-- ci.yml
|-- Dockerfile
|-- README.md
|-- requirements.txt
|-- .dockerignore
|-- .gitignore
|-- .venv310/
```

Recommended submission focus:

- Main notebook: `notebooks/smart_education_analytics_q1_q7.ipynb`
- Main documentation: `docs/PROJECT_DOCUMENTATION.md`
- Input datasets: files inside `data/`, kept local and ignored by Git
- Prompt file: `docs/Case Study8.pdf`
- Generated outputs: files inside `outputs/`
- Docker artifact: `Dockerfile`
- Kubernetes artifacts: `k8s/deployment.yaml`, `k8s/service.yaml`
- CI/CD artifact: `.github/workflows/ci.yml`
- Run helper scripts: files inside `src/`

Note: `.venv310/` is the local environment used to run this project. It is useful for running locally, but it is usually not uploaded to GitHub.

## Data Source and Data Loading

The data was already available locally and was organized into the project `data/` folder. The provided files match the Open University Learning Analytics Dataset (OULAD).

Dataset source link:

```text
https://figshare.com/articles/dataset/OULAD_Open_University_Learning_Analytics_Dataset/5081998?file=8606371
```

Dataset CSV files are intentionally ignored by Git because they are local input data and `studentVle.csv` is very large.

The notebook loads these CSV files using Spark:

| Dataset | Rows | Columns | Purpose |
|---|---:|---:|---|
| `assessments.csv` | 206 | 6 | Assessment metadata such as type, date, and weight |
| `courses.csv` | 22 | 3 | Course and presentation length details |
| `studentAssessment.csv` | 173,912 | 5 | Student assessment submissions and scores |
| `studentInfo.csv` | 32,593 | 12 | Student demographics and final result |
| `studentRegistration.csv` | 32,593 | 5 | Registration and unregistration dates |
| `vle.csv` | 6,364 | 6 | Virtual learning environment activity metadata |
| `studentVle.csv` | 10,655,280 | 6 | Student click/activity logs |

Spark loading code uses:

```python
spark.read.option("header", True).option("inferSchema", True).option("nullValue", "").csv(...)
```

This keeps the workflow beginner-friendly while still letting Spark infer useful data types.

## Environment Setup

Two virtual environments were created during setup, but only one is required now:

- `.venv310`: final working Python 3.10 environment used to execute the notebook.

The final successful execution used `.venv310` because PySpark 3.5 worked more reliably with Python 3.10 on this Windows system.

Main packages installed:

- `pyspark==3.5.7`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `nbformat`
- `nbclient`
- `ipykernel`
- `pypdf`
- `setuptools`

Important environment variables were used while executing:

```powershell
$env:PYSPARK_PYTHON = ".venv310\Scripts\python.exe"
$env:PYSPARK_DRIVER_PYTHON = ".venv310\Scripts\python.exe"
```

This was needed because Spark was otherwise trying to use `python3`, which was not available on Windows.

## Notebook Flow

### Q1. Spark Initialization and Data Loading

The notebook initializes Spark in local mode:

```python
SparkSession.builder.appName("SmartEducationAnalyticsQ1toQ7").master("local[*]")
```

Then it loads all seven CSV datasets and prints:

- Dataset row counts
- Column counts
- Full Spark schemas
- Sample student information
- Sample VLE activity records

Output confirmed all datasets loaded successfully.

### Q2. RDD Implementation

RDD operations were performed using `student_info.rdd`.

Operations included:

- `map`
- `filter`
- `reduceByKey`
- `sortBy`
- `take`
- `collect`

Important output:

```text
Final result counts:
Pass: 12361
Withdrawn: 10156
Fail: 7052
Distinction: 3024
```

Top regions by student count:

```text
Scotland: 3446
East Anglian Region: 3340
London Region: 3216
South Region: 3092
North Western Region: 2906
```

### Q3. Key-Value Operations and Persistence

Key-value RDD operations were applied on assessment scores.

Main steps:

- Created `(id_assessment, score)` key-value pairs.
- Reduced scores by assessment.
- Joined average assessment scores with assessment metadata.
- Persisted click summary using `MEMORY_AND_DISK`.

Example output:

```text
Assessment 1752 average score: 70.31, module AAA, type TMA, weight 10
Assessment 1758 average score: 69.26, module AAA, type TMA, weight 10
```

Student click summary:

```text
Persisted student click summary rows: 29228
```

Highest total clicks example:

```text
Student 80868, module CCC, presentation 2014J, total clicks 24139
```

### Q4. Spark DataFrame Operations

DataFrame joins and aggregations were used to build a student-level profile.

Joined tables:

- `student_info`
- `student_registration`
- `courses`
- assessment score aggregates
- VLE click aggregates

Created columns:

- `avg_score`
- `weighted_avg_score`
- `assessments_submitted`
- `banked_assessments`
- `total_clicks`
- `activity_rows`

Output:

```text
Student profile rows: 32593
```

Average score and clicks by module:

| Module | Students | Avg Score | Avg Clicks |
|---|---:|---:|---:|
| AAA | 712 | 64.27 | 1666.65 |
| BBB | 7692 | 56.32 | 661.80 |
| CCC | 4251 | 51.66 | 1055.97 |
| DDD | 5848 | 53.22 | 881.71 |
| EEE | 2859 | 62.71 | 1357.95 |
| FFF | 7397 | 61.21 | 2266.67 |
| GGG | 2525 | 64.47 | 526.39 |

### Q5. Exploratory Data Analysis and Spark SQL

Spark SQL views were created for all major tables.

EDA checks included:

- Missing values
- Duplicate student keys
- Student result distribution
- Score and engagement analysis

Important missing-value findings:

- `assessments.date`: 11 missing values
- `studentAssessment.score`: 173 missing values
- `studentInfo.imd_band`: 1111 missing values
- `studentRegistration.date_registration`: 45 missing values
- `studentRegistration.date_unregistration`: 22521 missing values
- `vle.week_from` and `vle.week_to`: 5243 missing values each
- `studentVle`: no missing values found

Duplicate key checks:

```text
student_info duplicate student-course keys: none
student_registration duplicate student-course keys: none
```

Spark SQL queries answered:

1. Online attendance or engagement pattern using VLE clicks.
2. Subject-wise performance.
3. Top-performing students.
4. Placement trend proxy using final academic outcome.
5. Semester-wise academic report.

Subject-wise performance output:

| Module | Assessed Students | Avg Score | Min Score | Max Score |
|---|---:|---:|---:|---:|
| EEE | 2267 | 81.18 | 0.0 | 100.0 |
| GGG | 2104 | 79.70 | 0.0 | 100.0 |
| FFF | 6052 | 77.71 | 0.0 | 100.0 |
| BBB | 5955 | 76.71 | 0.0 | 100.0 |
| CCC | 3317 | 73.26 | 0.0 | 100.0 |
| DDD | 4695 | 70.09 | 0.0 | 100.0 |
| AAA | 677 | 69.03 | 0.0 | 98.0 |

Semester-wise academic reports were generated by `code_presentation` and `code_module`, including:

- student count
- distinction count
- pass count
- fail count
- withdrawn count
- average weighted score
- average clicks

### Q6. ETL Pipeline Development

The ETL pipeline built a final student feature table for machine learning.

Feature engineering steps:

- Aggregated VLE activity by student.
- Counted active learning days.
- Calculated first and last activity day.
- Calculated `days_registered_before_start`.
- Created `was_unregistered` binary flag.
- Created `pass_label` target:
  - `1.0` for `Pass` and `Distinction`
  - `0.0` for `Fail` and `Withdrawn`
- Filled missing numeric values with 0.
- Saved the final table to CSV.

Final ETL output:

```text
ETL feature table rows: 32593
Saved file: outputs/student_features.csv
```

Label distribution:

| Label | Final Result | Count |
|---:|---|---:|
| 0.0 | Fail | 7052 |
| 0.0 | Withdrawn | 10156 |
| 1.0 | Distinction | 3024 |
| 1.0 | Pass | 12361 |

### Q7. Machine Learning Implementation

The notebook trains a Spark ML Logistic Regression model.

Target:

```text
pass_label = 1 for Pass/Distinction, 0 for Fail/Withdrawn
```

Categorical features:

- `code_module`
- `code_presentation`
- `gender`
- `region`
- `highest_education`
- `imd_band`
- `age_band`
- `disability`

Numeric features:

- `num_of_prev_attempts`
- `studied_credits`
- `module_presentation_length`
- `days_registered_before_start`
- `was_unregistered`
- `avg_score`
- `weighted_avg_score`
- `assessments_submitted`
- `banked_assessments`
- `total_clicks`
- `active_days`
- `avg_clicks_per_day`

ML pipeline stages:

1. `StringIndexer`
2. `OneHotEncoder`
3. `VectorAssembler`
4. `LogisticRegression`

Train-test split:

```text
Train rows: 26240
Test rows: 6353
```

Model results:

| Metric | Value |
|---|---:|
| AUC | 0.9706 |
| Accuracy | 0.9142 |
| F1 Score | 0.9142 |

Confusion matrix:

| Actual Label | Prediction | Count |
|---:|---:|---:|
| 0.0 | 0.0 | 2936 |
| 0.0 | 1.0 | 400 |
| 1.0 | 0.0 | 145 |
| 1.0 | 1.0 | 2872 |

Saved ML output files:

- `outputs/model_metrics.json`
- `outputs/sample_predictions.csv`

## Generated Output Files

### `outputs/student_features.csv`

Final ETL table with 32,593 student-course records.

Important columns include:

- student demographics
- course and presentation details
- assessment score features
- VLE engagement features
- registration features
- `pass_label`

### `outputs/model_metrics.json`

Contains the model evaluation metrics:

```json
{
  "model": "Spark ML Logistic Regression",
  "target": "pass_label",
  "auc": 0.9706097899274218,
  "accuracy": 0.9142137572800252,
  "f1": 0.9142484488670111
}
```

### `outputs/sample_predictions.csv`

Contains sample prediction outputs with:

- actual label
- predicted label
- prediction probability
- selected input features

## Challenges Faced and Solutions

### Challenge 1: Network restriction during package installation

Initial `pip install` failed because network access was restricted.

Solution:

Package installation was rerun with approved network access, and required packages were installed inside the project virtual environment.

### Challenge 2: PySpark with Python 3.12 failed on `distutils`

PySpark 3.5 tried importing `distutils`, which is not available by default in Python 3.12.

Solution:

`setuptools` was installed, but a better final solution was to use Python 3.10 because it worked more reliably with PySpark 3.5.

### Challenge 3: Spark worker tried to use `python3`

On Windows, Spark tried to start workers using `python3`, but `python3` was not available.

Error symptom:

```text
Python was not found; run without arguments to install from the Microsoft Store
```

Solution:

Explicitly set:

```powershell
$env:PYSPARK_PYTHON = ".venv310\Scripts\python.exe"
$env:PYSPARK_DRIVER_PYTHON = ".venv310\Scripts\python.exe"
```

After this, RDD operations and Spark ML worked correctly.

### Challenge 4: Matplotlib cache permission issue

Matplotlib attempted to write cache files in the user profile and hit a permission issue.

Solution:

Set `MPLCONFIGDIR` to a project-local folder:

```text
outputs/matplotlib_cache/
```

### Challenge 5: Spark Parquet/model saving failed because Hadoop `winutils.exe` was missing

On Windows, Spark file writes to Parquet/model directories can require Hadoop `winutils.exe` or `HADOOP_HOME`.

Error symptom:

```text
HADOOP_HOME and hadoop.home.dir are unset
```

Solution:

To keep the notebook executable without installing Hadoop binaries:

- ETL output was saved as `outputs/student_features.csv` using pandas.
- Model metrics were saved as `outputs/model_metrics.json`.
- Sample predictions were saved as `outputs/sample_predictions.csv`.
- The trained Spark model was kept in memory during the notebook run.

### Challenge 6: Kubernetes could not mount the local Windows data folder

Docker Desktop Kubernetes did not recognize the attempted Windows hostPath mount for the local `data/` folder.

Error symptom:

```text
hostPath type check failed: .../case_study/data is not a directory
```

Solution:

For the local Kubernetes demonstration, the Docker image was built with the local ignored CSV files copied into `/app/data`. The CSV files remain ignored by Git, so they are not uploaded to GitHub.

### Challenge 7: Kubernetes reused an older cached `latest` image

The pod initially failed with:

```text
FileNotFoundError: data/ folder not found
```

The rebuilt local image contained `/app/data`, but Kubernetes was still using an older cached image for the `latest` tag.

Solution:

The Kubernetes deployment was changed to use a fresh local tag:

```text
smart-education-analytics:k8s-final-v2
```

This forced Docker Desktop Kubernetes to use the corrected image.

### Challenge 8: Running the full Spark notebook during pod startup was too heavy

The first Kubernetes command ran:

```text
python src/run_notebook.py && python -m http.server 8080 --directory outputs
```

This made the pod spend a long time running Spark before the HTTP service became useful.

Solution:

The Kubernetes command was changed to:

```text
python src/health_check.py && python -m http.server 8080 --directory outputs
```

This is a better deployment flow because notebook execution is already validated separately, while Kubernetes checks the packaged project and serves the generated output artifacts.

## How to Run

Use the Python 3.10 environment:

```powershell
cd C:\Users\15dha\OneDrive\Desktop\case_study

$env:PYSPARK_PYTHON=(Resolve-Path ".\.venv310\Scripts\python.exe").Path
$env:PYSPARK_DRIVER_PYTHON=$env:PYSPARK_PYTHON

.\.venv310\Scripts\python -m jupyter notebook
```

Then open:

```text
notebooks/smart_education_analytics_q1_q7.ipynb
```

The notebook has already been executed and saved with outputs.

## Additional Submission Artifacts After Q7

The case-study PDF also asks for version control, Docker, Kubernetes, CI/CD, screenshots, and final documentation. The following local artifacts have been created:

| Requirement | Local Status | File or Folder |
|---|---|---|
| README documentation | Created | `README.md` |
| Dependency list | Created | `requirements.txt` |
| Dockerfile | Created | `Dockerfile` |
| Kubernetes deployment YAML | Created | `k8s/deployment.yaml` |
| Kubernetes service YAML | Created | `k8s/service.yaml` |
| CI/CD pipeline | Created | `.github/workflows/ci.yml` |
| Notebook runner script | Created | `src/run_notebook.py` |
| Project health check script | Created | `src/health_check.py` |
| Screenshot folders | Created | `screenshots/` |

Final submission status:

| Requirement | Current status |
|---|---|
| GitHub repository | Project pushed to GitHub. |
| Docker execution | Docker image build and run validated locally. |
| Kubernetes execution | Docker Desktop Kubernetes deployment validated locally. |
| CI/CD | GitHub Actions workflow validated on push. |
| Screenshots | Keep screenshots in `screenshots/docker/`, `screenshots/kubernetes/`, and `screenshots/github_actions/` if required by the evaluator. |

Docker commands:

```powershell
docker build -t smart-education-analytics:latest .
docker run --rm -v ${PWD}\outputs:/app/outputs smart-education-analytics:latest
```

Kubernetes commands:

```powershell
docker build -t smart-education-analytics:latest -t smart-education-analytics:k8s-final-v2 .
kubectl apply -f k8s\deployment.yaml
kubectl apply -f k8s\service.yaml
kubectl get pods
kubectl get svc
kubectl logs deployment/smart-education-analytics
```

## End-to-End Code Flow

```text
Case Study PDF in docs/ + CSV files in data/
        |
        v
Spark session initialization
        |
        v
Load all CSV files as Spark DataFrames
        |
        v
Inspect row counts, schemas, and sample records
        |
        v
RDD operations for result counts and region analysis
        |
        v
Key-value RDD operations on assessment scores
        |
        v
DataFrame joins:
student_info + registration + courses + assessments + VLE clicks
        |
        v
Spark SQL EDA:
attendance proxy, subject performance, top students, outcome trends, semester reports
        |
        v
ETL feature table creation
        |
        v
Spark ML pipeline:
StringIndexer -> OneHotEncoder -> VectorAssembler -> LogisticRegression
        |
        v
Model evaluation:
AUC, accuracy, F1, confusion matrix
        |
        v
Save output files in outputs/
```

## Final Status

The notebook was executed successfully from top to bottom.

Validation result:

```text
Executed code cells: 12
Notebook error outputs: 0
```

The final solution covers Q1 to Q7 of the case study using the available datasets and saves the generated output files in the `outputs/` folder.
