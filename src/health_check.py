from __future__ import annotations

import argparse
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROJECT_REQUIRED_PATHS = [
    "data/README.md",
    "docs/Case Study8.pdf",
    "docs/PROJECT_DOCUMENTATION.md",
    "notebooks/smart_education_analytics_q1_q7.ipynb",
    "outputs/model_metrics.json",
    "README.md",
    "Dockerfile",
    "requirements.txt",
    "k8s/deployment.yaml",
    "k8s/service.yaml",
]

DATA_PATHS = [
    "data/assessments.csv",
    "data/courses.csv",
    "data/studentAssessment.csv",
    "data/studentInfo.csv",
    "data/studentRegistration.csv",
    "data/vle.csv",
    "data/studentVle.csv",
]


def check_required_paths(skip_data: bool) -> list[str]:
    paths = PROJECT_REQUIRED_PATHS.copy()
    if not skip_data:
        paths.extend(DATA_PATHS)

    return [rel_path for rel_path in paths if not (PROJECT_ROOT / rel_path).exists()]


def check_metrics() -> dict[str, float | str]:
    metrics_path = PROJECT_ROOT / "outputs" / "model_metrics.json"
    with metrics_path.open("r", encoding="utf-8") as f:
        metrics = json.load(f)

    for key in ["model", "target", "auc", "accuracy", "f1"]:
        if key not in metrics:
            raise ValueError(f"Missing metric key: {key}")

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Check project files and output metrics.")
    parser.add_argument("--skip-data", action="store_true", help="Skip checking local dataset files in CI.")
    parser.add_argument("--skip-large-data", action="store_true", help="Deprecated alias for --skip-data.")
    args = parser.parse_args()

    missing = check_required_paths(skip_data=args.skip_data or args.skip_large_data)
    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))

    metrics = check_metrics()
    print("Project structure check passed.")
    print("Model:", metrics["model"])
    print("AUC:", metrics["auc"])
    print("Accuracy:", metrics["accuracy"])
    print("F1:", metrics["f1"])


if __name__ == "__main__":
    main()
