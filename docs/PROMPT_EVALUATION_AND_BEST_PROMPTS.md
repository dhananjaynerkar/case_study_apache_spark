# Prompt Evaluation and Better Prompting Guide

This file evaluates the prompt style used during the project and gives improved prompts that would reduce confusion, repeated commands, unnecessary compute, and wasted time.

I am not using an exact exported prompt count from the app. This evaluation is based on the visible prompt pattern in the project conversation.

## 1. Main Prompting Mistakes

### Mistake 1: Asking in small fragments

Example pattern:

```text
next
what to do now
still
do it
```

### Problem

Short prompts are fast to type, but they often miss context. The assistant then has to inspect again or ask/answer step by step.

### Better approach

Give current state, command output, and expected goal in one message.

## 2. Mistake 2: Pasting terminal logs mixed with commands

Example pattern:

```text
cd ...
>> 0.9142484488670111
>> git add -A screenshotsort 8080 ...
```

### Problem

Logs and commands got mixed together. This can create invalid commands and makes debugging harder.

### Better approach

Paste commands and outputs separately:

```text
Command I ran:
git push origin main

Output:
...

What should I do next?
```

## 3. Mistake 3: Asking for execution without giving success criteria

Example:

```text
complete task
```

### Problem

The assistant can complete the main task, but final expectations like zip size, screenshots, GitHub push, or dataset upload policy may be unclear.

### Better approach

State exactly what should be considered complete.

## 4. Mistake 4: Changing direction after work was done

Example pattern:

1. Upload datasets to Git.
2. Then remove datasets from Git.
3. Then add dataset link.
4. Then create zip under 100 MB.

### Problem

This causes repeated Git commits, changed documentation, and repeated zip creation.

### Better approach

Mention constraints early:

```text
Upload limit is 100 MB. Do not include raw CSV files. Add dataset link instead.
```

## 5. Mistake 5: Not separating local execution from submission requirement

### Problem

Docker and Kubernetes need local data, but GitHub and zip should avoid large raw datasets.

### Better approach

Say:

```text
Keep data local for execution, but do not include raw CSV files in GitHub or final zip.
```

## 6. Mistake 6: Asking "is this right" without naming the requirement

Example:

```text
is this screenshot right?
```

### Problem

The assistant has to infer whether the screenshot is for Docker, Kubernetes, GitHub Actions, or project output.

### Better approach

```text
Is this screenshot valid for the Kubernetes deployment requirement? It shows pod 1/1 Running, service, deployment, and logs.
```

## 7. Best Criteria for Good Prompts

Use this checklist:

| Criteria | Good prompt should include |
|---|---|
| Goal | What final result you want |
| Current state | What already exists or what command was run |
| Error/output | Exact terminal output if debugging |
| Constraint | Size limit, no dataset upload, deadline, specific format |
| Scope | Whether to edit files, just advise, or create zip |
| Verification | What success should look like |

## 8. How Better Prompts Reduce Carbon Emission

AI and cloud tools consume electricity. Better prompts help because they reduce:

- repeated file inspection
- repeated Docker builds
- repeated Kubernetes deployments
- unnecessary Git commits
- repeated notebook execution
- long back-and-forth clarification

This saves time, compute, electricity, and indirectly reduces carbon emission. It also helps the country by reducing wasted digital infrastructure usage and improving engineering discipline.

## 9. Best Prompt for This Entire Case Study

Use this instead of many small prompts:

```text
I have Case Study 8: Smart Education Analytics using Apache Spark. Work in this folder:
C:\Users\15dha\OneDrive\Desktop\case_study

Please inspect the project first. Then complete the project end-to-end with these requirements:

1. Solve Q1-Q7 in one executed Jupyter notebook using PySpark.
2. Use the provided OULAD CSV files from data/.
3. Do not upload raw CSV datasets to GitHub or final zip because upload limit is 100 MB.
4. Add the dataset source link in README, data README, and documentation:
   https://figshare.com/articles/dataset/OULAD_Open_University_Learning_Analytics_Dataset/5081998?file=8606371
5. Create a clean folder structure.
6. Generate outputs: student_features.csv, model_metrics.json, sample_predictions.csv.
7. Create README and final project documentation.
8. Add Dockerfile and verify Docker build/run.
9. Add Kubernetes deployment and service YAML and verify deployment on Docker Desktop Kubernetes.
10. Add GitHub Actions workflow for project validation.
11. Add screenshot folders and tell me exactly what screenshots are required.
12. Create a submit/ folder and submit.zip under 100 MB.
13. Commit and push only source, docs, outputs, screenshots, and configs. Do not commit raw CSV files, virtualenvs, or submit.zip.

For every major step, give me:
- command used
- purpose
- success criteria
- files changed
- validation result
```

## 10. Better Prompts for Each Phase

### Prompt 1: Initial project setup

```text
Inspect this project folder and create a clean file structure for the Spark case study. Keep datasets in data/ but do not commit raw CSV files. Add .gitignore before any Git commit.
```

### Prompt 2: Notebook execution

```text
Read the case-study PDF and available CSV files. Create and execute one notebook that solves Q1-Q7 using PySpark. Save outputs in outputs/. Do not hallucinate columns; inspect the CSV schemas first.
```

### Prompt 3: Documentation

```text
Create documentation explaining data source, data loading, transformations, Spark SQL analysis, ETL, ML model, outputs, challenges, solutions, and final file structure.
```

### Prompt 4: GitHub preparation

```text
Prepare this project for GitHub. Ensure raw CSV datasets, virtual environments, caches, and submit.zip are ignored. Only keep data/README.md with dataset link and required file list.
```

### Prompt 5: Docker

```text
Create and test a Dockerfile for this PySpark project. Give me build/run commands, expected success output, and screenshot requirement.
```

### Prompt 6: Kubernetes

```text
Create Kubernetes deployment and service YAML for Docker Desktop Kubernetes. Verify pod, service, deployment, and logs. Avoid using latest tag if Kubernetes caches old images.
```

### Prompt 7: CI/CD

```text
Create a GitHub Actions workflow that installs dependencies, runs project health checks, validates Kubernetes YAML, and optionally builds the Docker image if it can run without raw datasets.
```

### Prompt 8: Final zip

```text
Create a submit/ folder and submit.zip below 100 MB. Include source, notebook, docs, outputs, Dockerfile, Kubernetes YAML, CI workflow, screenshots, and data/README.md. Exclude raw CSV files, .git, virtual environments, and caches.
```

## 11. Best Way to Ask Debugging Questions

Use this template:

```text
I ran this command:
<command>

Expected:
<what I expected>

Actual output/error:
<paste exact output>

Project constraint:
<for example: do not upload datasets, zip under 100 MB>

Please explain root cause first, then give the smallest correct fix and verification command.
```

## 12. Final Prompting Lesson

The best prompt is not the longest prompt. The best prompt gives the correct context once, includes constraints early, and asks for verification. This reduces repeated work and makes the final project easier to explain.

