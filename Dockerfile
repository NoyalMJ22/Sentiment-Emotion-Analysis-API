FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install basic dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir pip==23.3.1
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download huggingface models to cache them in the Docker image
# This prevents downloading large files on every application restart
RUN python -c "from transformers import pipeline; \
pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english'); \
pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base')"

# Copy remaining application code
COPY ./app /app/app

# Expose port
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
