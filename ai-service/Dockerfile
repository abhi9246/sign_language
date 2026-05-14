# ---- AI Microservice (Python Flask + TensorFlow + MediaPipe) ----
FROM python:3.11-slim

# Install system dependencies for OpenCV and enchant
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libenchant-2-dev \
    aspell-en \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model
COPY predict_service.py .
COPY cnn8grps_rad1_model.h5 .

# Expose the AI service port
EXPOSE 5001

ENV PREDICT_HOST=0.0.0.0
ENV PREDICT_PORT=5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5001/')" || exit 1

CMD ["python", "predict_service.py"]
