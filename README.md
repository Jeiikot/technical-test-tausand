# Tausand Technical Test — Python Developer

Technical assessment for the Python Developer position at **Tausand Electrónica**.

---

## Exercises

### Exercise 1: Cumulative Sum with Live Graph

A PyQt5 + pyqtgraph desktop application that captures numeric key presses (1-5), displays the running cumulative sum, and plots a real-time step-function graph over a 30-second sliding window.

**[Go to Exercise 1](exercise_1_cumulative_sum/)**

### Exercise 2: TempicoSoftware — Execution & Editing

Clone, run, and modify the [TempicoSoftware](https://github.com/Tausand-dev/TempicoSoftware) application. Changes include adding an "About Me" button and editing the About dialog content.

**[Go to Exercise 2](exercise_2_tempico_software/)**

---

## Prerequisites

- **Python 3.9+** (Python 3.9 recommended for PySide2 compatibility in Exercise 2)
- **Linux** (tested on Ubuntu)
- **[uv](https://docs.astral.sh/uv/)** (recommended) or **pip**

## Quick Start

### Exercise 1
```bash
cd exercise_1_cumulative_sum
uv sync                  # install dependencies
uv run python main.py    # run the application
```

### Exercise 2
```bash
cd exercise_2_tempico_software/TempicoSoftware
pip install -r requirements.txt    # PySide2 requires Python 3.9
python src/main.py
```

---

## Time Report

See [time_report.md](time_report.md) for a detailed breakdown of time spent on each task.

## Repository Structure

```
tausand-technical-test/
├── README.md                          # This file
├── .gitignore
├── time_report.md                     # Time tracking report
├── exercise_1_cumulative_sum/
│   ├── README.md                      # Exercise 1 documentation
│   ├── pyproject.toml                 # uv project config & dependencies
│   ├── uv.lock                        # Dependency lockfile
│   ├── requirements.txt               # Fallback pip requirements
│   ├── main.py                        # Application source code
│   └── screenshots/                   # Application screenshots
├── exercise_2_tempico_software/
│   ├── README.md                      # Exercise 2 documentation
│   ├── TempicoSoftware/               # Cloned + modified repo
│   └── screenshots/                   # Application screenshots
```
