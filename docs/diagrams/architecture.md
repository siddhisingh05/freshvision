# Architecture Diagram

```
Browser (Bootstrap 5 + Jinja2)
        |
        | HTTP
        v
Flask App (AWS EC2 + Docker)
  ├── routes/main.py      → index.html, about.html
  ├── routes/predict.py   → predict.html, result.html
  └── routes/history.py   → history.html
        |
        ├── utils/preprocess.py  (PIL image resize + normalize)
        ├── utils/inference.py   (TensorFlow MobileNetV2 model)
        └── models/database.py   (SQLite — predictions table)
                |
        freshness.db (SQLite file, local)
        ml/models/freshness_model.h5 (downloaded from AWS S3 on startup)
```

TODO: Replace with a proper PNG diagram (use draw.io or Excalidraw → export PNG → save here).
