# 🥦 Food Freshness Classification System

> A Full-Stack · AI/ML · Cloud-Deployed system for automated food freshness detection

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-FF6F00?logo=tensorflow)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2+S3-FF9900?logo=amazonaws)

**Live Demo:** [http://your-ec2-ip:5000](#) &nbsp;|&nbsp; **Course:** ML Mini Project — 3 Academic Credits

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [ML Model](#ml-model)
- [Cloud Deployment](#cloud-deployment)
- [Screenshots](#screenshots)
- [Team](#team)

---

## Overview

FreshnessAI is a **unified AI-based food freshness classification system** that assesses the freshness of fruits, vegetables, meat, and dairy products from a single uploaded image using deep learning.

**Freshness Classes:** `Fresh` &nbsp;·&nbsp; `Moderately Fresh` &nbsp;·&nbsp; `Spoiled`

**Key capabilities:**
- Drag-and-drop image upload with instant classification
- Confidence scores with visual progress bars for each class
- Prediction history dashboard with summary statistics
- Feedback loop to record corrections for future retraining
- Fully containerised with Docker, deployed on AWS EC2

---

## System Architecture

```
User Browser
     │
     │  HTTP (Bootstrap + Jinja2 pages)
     ▼
Flask Web App  ──────────────────────────────┐
 ├── /          (Home)                        │
 ├── /predict   (Upload + classify)           │  SQLite DB
 ├── /history   (Past predictions)            │  freshness.db
 └── /about     (Project info)                │
     │                                        │
     │  TensorFlow model inference             │
     ▼                                        │
MobileNetV2 Model  ◄── ml/models/ (from S3) ──┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10, Flask 3.0, Gunicorn |
| Frontend | Jinja2 Templates, Bootstrap 5, Bootstrap Icons |
| AI / ML | TensorFlow 2.13, MobileNetV2 (Transfer Learning) |
| Database | SQLite (Flask built-in) |
| Cloud | AWS EC2 (hosting), AWS S3 (model storage) |
| CI/CD | GitHub Actions |
| Containerisation | Docker, Docker Compose |

---

## Project Structure

```
freshness-classifier/
│
├── run.py                      # App entry point
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Local dev + production orchestration
├── .gitignore
│
├── app/                        # Flask application package
│   ├── __init__.py             # App factory (create_app)
│   ├── routes/
│   │   ├── main.py             # Home + About pages
│   │   ├── predict.py          # Image upload + model inference
│   │   └── history.py          # Prediction history
│   ├── models/
│   │   └── database.py         # SQLite init + get_db helper
│   ├── utils/
│   │   ├── preprocess.py       # Image resize + normalize
│   │   └── inference.py        # Load model + run prediction
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── uploads/            # Uploaded images (gitignored)
│   └── templates/
│       ├── base.html           # Shared navbar + layout
│       ├── index.html          # Home page
│       ├── predict.html        # Upload form
│       ├── result.html         # Prediction result
│       ├── history.html        # History dashboard
│       └── about.html
│
├── ml/                         # Machine Learning
│   ├── scripts/
│   │   ├── train.py            # Model training pipeline
│   │   ├── evaluate.py         # Metrics + confusion matrix
│   │   └── preprocess.py       # Dataset preprocessing + splitting
│   ├── notebooks/
│   │   ├── 01_eda.ipynb        # Exploratory data analysis
│   │   └── 02_training.ipynb   # Training walkthrough
│   ├── models/                 # Saved .h5 files (gitignored, stored in S3)
│   └── data/
│       ├── raw/                # Downloaded dataset (gitignored)
│       └── processed/          # Train/val/test splits (gitignored)
│
├── tests/
│   └── test_routes.py          # Pytest route tests
│
├── cloud/
│   ├── docker/Dockerfile       # Production Docker image
│   ├── aws/ec2-setup.sh        # EC2 bootstrap script
│   └── .github/workflows/
│       └── deploy.yml          # CI/CD: test → build → deploy
│
└── docs/
    ├── api/endpoints.md
    └── diagrams/architecture.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- Docker (optional but recommended)

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/freshness-classifier.git
cd freshness-classifier
```

### 2. Install & Run (local)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open **http://localhost:5000**

### 3. Run with Docker

```bash
docker-compose up --build
```

---

## ML Model

| Detail | Value |
|---|---|
| Base model | MobileNetV2 (pretrained ImageNet) |
| Fine-tuned on | Fruits & Vegetables Freshness — Kaggle |
| Input | 224 × 224 RGB image |
| Output | 3-class softmax — Fresh / Moderately Fresh / Spoiled |
| Accuracy | ~XX% on test set *(update after training)* |

Training details: `ml/notebooks/02_training.ipynb`

---

## Cloud Deployment

| Component | Service | Status |
|---|---|---|
| Flask App | AWS EC2 (t2.micro / t2.medium) | 🟡 In Progress |
| Model Artifact | AWS S3 | 🟡 In Progress |
| CI/CD | GitHub Actions | 🟡 In Progress |

**Deploy to EC2:**
```bash
# On your EC2 instance:
bash cloud/aws/ec2-setup.sh
```

---

## Screenshots

> TODO: add screenshots of Home, Predict, Result, and History pages

---

## Team

| Name | Role |
|---|---|
| [Your Name] | ML + Full-Stack |
| [Member 2] | Backend / Deployment |
| [Member 3] | Frontend / Testing |

---

*Machine Learning Mini Project · 3 Academic Credits*
