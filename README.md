# FocalPoint AI

AI-powered image editor for background removal, bokeh effects, and person anonymization.

[Live Demo](https://focal-point-ai-rkt.streamlit.app/)

## Architecture

- **Backend**: FastAPI service running PyTorch models on GCP Cloud Run
- **Frontend**: Streamlit UI deployed on Streamlit Community Cloud
- **Models**: DeepLabV3 (v1) and Mask R-CNN (v2) for segmentation

## Versions

### v1: Semantic Segmentation (`v1-deeplab` branch)
Scene-level segmentation using DeepLabV3.

- Background removal
- Bokeh effect
- Full-image anonymization

### v2: Instance Segmentation (`v2-maskrcnn` branch)
Per-person segmentation using Mask R-CNN.

- Individual person selection
- Targeted effect application
- Face-only anonymization (two-stage pipeline: person detection → face detection)

## Setup

**Prerequisites**: Python 3.11+

1. **Clone and checkout version**
```bash
git clone https://github.com/your-username/FocalPointAI.git
cd FocalPointAI
git checkout v1-deeplab  # or v2-maskrcnn
```

2. **Backend**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

3. **Frontend** (new terminal)
```bash
source venv/bin/activate
streamlit run frontend.py
```

## Deployment

- **Backend**: Dockerized FastAPI on GCP Cloud Run
- **Frontend**: Streamlit Community Cloud
- **Communication**: Frontend → Backend via HTTP API

## Technical Decisions

**Model Selection**: DeepLabV3 for v1 provides fast semantic segmentation. Mask R-CNN for v2 enables instance-level control at the cost of increased latency.

**Deployment Split**: Heavy ML inference isolated in containerized backend. Lightweight Streamlit frontend communicates via API for better scalability.

**Image Optimization**: CPU-only PyTorch build reduces Docker image from 2GB+ to <1GB, significantly improving cold start times on Cloud Run.

## Key Implementation Details

- State management using Streamlit `session_state` to handle image uploads and effect persistence
- Two-stage anonymization pipeline in v2: Mask R-CNN person detection followed by face detection within bounding boxes for precise facial blurring
- Docker base image pinned to `python:3.11-slim` for reproducible builds

## Stack

- PyTorch / torchvision
- FastAPI
- Streamlit
- Docker
- GCP (Cloud Run, Artifact Registry)

## License

MIT