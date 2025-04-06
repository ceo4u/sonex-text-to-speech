# Change Python version to 3.11
FROM python:3.11-slim-bookworm

# Set CUDA version for PyTorch
ENV TORCH_CUDA_VERSION=cu118

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir --use-deprecated=legacy-resolver

# Copy the application code
COPY . .

# Create temp directory for audio processing
RUN mkdir -p /tmp/tts_audio && chmod 777 /tmp/tts_audio
ENV TEMP_DIR=/tmp/tts_audio

# Expose port
EXPOSE 8000

# Start application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "--workers", "2", "tts_app:app"]
