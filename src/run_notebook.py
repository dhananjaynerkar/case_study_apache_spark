from __future__ import annotations

import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "smart_education_analytics_q1_q7.ipynb"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main() -> None:
    if not NOTEBOOK_PATH.exists():
        raise FileNotFoundError(f"Notebook not found: {NOTEBOOK_PATH}")

    if not (PROJECT_ROOT / "data").exists():
        raise FileNotFoundError("data/ folder not found. Add the provided CSV files before running.")

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "ipython").mkdir(exist_ok=True)
    (OUTPUT_DIR / "jupyter").mkdir(exist_ok=True)

    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["IPYTHONDIR"] = str(OUTPUT_DIR / "ipython")
    os.environ["JUPYTER_CONFIG_DIR"] = str(OUTPUT_DIR / "jupyter")

    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=1200,
        kernel_name="python3",
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    client.execute()
    nbformat.write(notebook, NOTEBOOK_PATH)
    print(f"Executed and saved: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
