# Sentiment & Emotion Analysis API

A production-ready FastAPI backend for advanced sentiment and emotion analysis using HuggingFace Transformers.

## Features:
- 🚀 **FastAPI**: Asynchronous routing, built-in validation, and auto-swagger docs.
- 🧠 **HuggingFace Models**: 
  - Sentiment Analysis (distilbert-base-uncased-finetuned-sst-2-english)
  - Emotion Recognition (j-hartmann/emotion-english-distilroberta-base)
- ⚡ **Batch Processing Support**: Process multiple sentences in parallel asynchronously.
- 🌍 **Language Detection**: Automatically detects language using `langdetect`.
- 🕒 **Caching**: LRU caching using `cachetools` to avoid re-evaluating equivalent inputs.
- 🚦 **Rate Limiting**: Includes token-bucket API rate limiting per IP using `slowapi`.

## 1. Local Setup

### Requirements
- Python 3.9+

### Installation

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python -m uvicorn app.main:app --reload
```
*Note: The first run might take a minute as it downloads the model weights (~600MB total).*

The API will be available at: http://localhost:8000  
Swagger Interactive Docs: http://localhost:8000/docs

## 2. API Usage Examples

### Single Text Analysis
**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "I absolutely love this product! It exceeded all my expectations."
}'
```

**Response:**
```json
{
  "text": "I absolutely love this product! It exceeded all my expectations.",
  "language": "en",
  "sentiment": "positive",
  "confidence": 0.9998,
  "emotions": {
    "joy": 0.9572,
    "surprise": 0.0211,
    "neutral": 0.0104,
    "anger": 0.0035,
    "sadness": 0.0033,
    "disgust": 0.0028,
    "fear": 0.0017
  }
}
```

### Batch Text Analysis
**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/analyze/batch' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "texts": [
    "This is amazing!",
    "I am very disappointed with the service."
  ]
}'
```

## 3. Project Structure
```
.
├── Dockerfile              # Docker settings
├── requirements.txt        # Python dependencies
└── app/
    ├── __init__.py
    ├── main.py             # FastAPI App instance
    ├── api/
    │   └── routes.py       # API Endpoints
    ├── core/
    │   ├── config.py       # Pydantic Settings
    │   └── logger.py       # Logging config
    ├── models/
    │   └── schemas.py      # Input/Output structures
    └── services/
        └── analyzer.py     # AI Pipeline Wrapper
```

## 4. Deployment Instructions

### Option A: Railway (Easiest)
Railway natively supports Dockerfiles.
1. Push this directory to a GitHub repository.
2. Go to [Railway.app](https://railway.app/), create an account, and connect your GitHub.
3. Click "New Project" -> Deploy from GitHub repo.
4. Railway will automatically detect the `Dockerfile` and build it.
5. In your Railway project service settings, set `PORT=8000` (though Railway detects EXPOSE usually).
6. Click Deploy. Note that downloading models takes memory. Ensure your deployment tier has at least 1-2GB RAM.

### Option B: Render Web Service
Render can also build using Docker.
1. Push this repository to GitHub.
2. Create an account on [Render.com](https://render.com).
3. Click "New" -> "Web Service".
4. Choose your repository.
5. In "Environment", choose "Docker".
6. Select your instance type (at least Starter tier recommended due to RAM requirements for HuggingFace Transformers, ~1.5GB RAM usage).
7. Deploy!
