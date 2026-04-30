# 🥦 FreshVision  — Food Freshness Classification System

> Full-Stack · AI/ML · Cloud-Deployed · GLA University ML Mini Project 2025-26

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-FF6F00?logo=tensorflow)](https://tensorflow.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://docker.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?logo=huggingface)](https://huggingface.co/spaces/Lazypanda0103/Unified-Comprehensive-Freshness-Classification)

**Live Demo (Gradio):** [huggingface.co/spaces/Lazypanda0103/Unified-Comprehensive-Freshness-Classification](https://huggingface.co/spaces/Lazypanda0103/Unified-Comprehensive-Freshness-Classification)  
**Flask App:** https://freshness-classifier.onrender.com  
**Course:** ML Mini Project · B.Tech CSE (AI/ML) Sem 4 ·

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

FreshVision is a **unified ML-based food freshness classification system** that assesses the freshness of fruits, vegetables, and produce from a single uploaded image using a two-stage deep learning pipeline.

**Freshness Classes:** `Fresh` · `Semi-Fresh` · `Rotten`

**Key capabilities:**
- Drag-and-drop image upload with instant classification
- Two-stage pipeline: YOLOv8 food detection + EfficientNetB0 classification
- Confidence scores with visual probability bars for each class
- User authentication (register/login) with bcrypt password hashing
- Prediction history dashboard with pagination and label filtering
- Feedback loop to record corrections for future retraining
- Fully containerised with Docker, deployed on Render.com + HuggingFace Spaces

---

## System Architecture

```
User Browser (Dark Theme UI — Syne + DM Mono fonts)
     │
     │  HTTP (Flask + Jinja2 templates)
     ▼
Flask Web App  ──────────────────────────────────────┐
 ├── /               (Home — hero + how it works)     │
 ├── /auth/login     (Sign in)                        │  SQLite DB
 ├── /auth/register  (Create account)                 │  freshness.db
 ├── /predict        (Upload + classify)              │  ├── users
 ├── /history        (Paginated prediction log)       │  ├── predictions
 ├── /feedback       (Label correction)               │  └── feedback
 └── /about          (Team + tech stack)              │
     │                                                │
     │  HuggingFace Gradio API call                   │
     ▼                 (local .h5 fallback)           │
YOLOv8 → EfficientNetB0 pipeline ───────────────────-┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10, Flask 3.0, Flask-Bcrypt, Gunicorn |
| Frontend | Jinja2 Templates, Bootstrap 5, Custom Dark CSS (Syne + DM Mono) |
| AI / ML | TensorFlow 2.13, YOLOv8, EfficientNetB0 (Transfer Learning) |
| Database | SQLite (parameterised queries throughout) |
| Cloud | Render.com (Flask app), HuggingFace Spaces (Gradio model) |
| CI/CD | GitHub Actions (lint → test → build) |
| Containerisation | Docker, Docker Compose |

---

## Project Structure

```
Mini_Project_/
│
├── run.py                          # App entry point
├── requirements.txt                # Python dependencies
├── docker-compose.yml              # Local dev + production orchestration
├── .gitignore
│
├── app/                            # Flask application package
│   ├── __init__.py                 # App factory, blueprint registration
│   ├── routes/
│   │   ├── auth.py                 # Register / login / logout (bcrypt)
│   │   ├── main.py                 # Home + About pages
│   │   ├── predict.py              # Image upload + inference + DB save
│   │   └── history.py              # Paginated history + feedback route
│   ├── models/
│   │   └── database.py             # SQLite schema: users, predictions, feedback
│   ├── utils/
│   │   ├── inference.py            # HF Gradio API call + local .h5 fallback
│   │   └── preprocess.py           # PIL resize 224×224, ImageNet normalisation
│   ├── static/
│   │   ├── css/style.css           # Custom dark design system
│   │   ├── js/main.js              # Drag-drop upload + DataTransfer injection
│   │   └── uploads/                # Uploaded images (gitignored)
│   └── templates/
│       ├── base.html               # Shared navbar + flash messages + footer
│       ├── index.html              # Hero + stats + how-it-works
│       ├── predict.html            # Drag-drop upload form
│       ├── result.html             # Prediction result + probability bars
│       ├── history.html            # Paginated history + feedback forms
│       ├── about.html              # Team + tech stack
│       └── auth/
│           ├── login.html
│           └── register.html
│
├── ml/                             # Machine Learning
│   ├── scripts/
│   │   ├── train.py                # EfficientNetB0 training pipeline
│   │   └── evaluate.py             # Metrics + confusion matrix
│   ├── notebooks/
│   │   └── FreshnessAI_Training.ipynb   # Full Colab training notebook
│   └── models/                     # Saved .h5 files (gitignored)
│
├── tests/
│   └── test_inference.py           # pytest — preprocess + inference unit tests
│
├── cloud/
│   ├── docker/Dockerfile           # Production Docker image (python:3.10-slim)
│   ├── aws/ec2-setup.sh            # EC2 bootstrap script
│   └── .github/workflows/
│       └── deploy.yml              # CI: pytest → docker build
│
└── docs/
    └── diagrams/                   # Architecture, ERD, sequence diagrams
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- Docker (optional)

### 1. Clone

```bash
git clone https://github.com/Lazy-Panda78/Mini_Project_.git
cd Mini_Project_
```

### 2. Install & Run locally

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
|--------|-------|
| Stage 1 | YOLOv8 — food region detection |
| Stage 2 | EfficientNetB0 — freshness classification |
| Pretrained on | ImageNet |
| Fine-tuned on | Kaggle Fruits Fresh & Rotten dataset |
| Input size | 224 × 224 RGB |
| Output | 3-class softmax — Fresh / Semi-Fresh / Rotten |
| Accuracy | 92% on test set |
| F1 Score | 0.91 |
| Live inference | HuggingFace Spaces Gradio API |

Training notebook: `ml/notebooks/FreshnessAI_Training.ipynb`

---

## Cloud Deployment

| Component | Service | Status |
|-----------|---------|--------|
| ML Model (Gradio) | HuggingFace Spaces | ✅ Live |
| Flask App | Render.com | ✅ Live |
| CI/CD | GitHub Actions | ✅ Active |

**HuggingFace Spaces (Gradio demo):**  
https://huggingface.co/spaces/Lazypanda0103/Unified-Comprehensive-Freshness-Classification

**Deploy Flask to Render:**
1. Connect repo at render.com
2. Runtime: Docker · Dockerfile: `./cloud/docker/Dockerfile`
3. Set env vars: `SECRET_KEY`, `HF_SPACE_URL`

---

## Screenshots

> Dashboard · Classify · Result · History pages — see `docs/screenshots/`

---

## Team

| Name | Role | Responsibilities |
|------|------|-----------------|
| Yash Upadhyay | ML Lead | Model training, HF deployment, inference pipeline, CI/CD |
| Siddhi Singh | Full-Stack Lead | Flask auth, routes, history, dark theme UI |
| Sanya Singh | Frontend / QA | UI polish, result page, testing, documentation |

---

*ML Mini Project · B.Tech CSE (AI/ML) · GLA University Mathura · 2025-26*
# freshvision
