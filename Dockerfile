# AI Virtual Try-On Application - Docker Container
# Multi-stage build for optimized production image

# =============================================================================
# STAGE 1: Base Python Environment
# =============================================================================

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# STAGE 2: Dependencies Installation
# =============================================================================

FROM base as dependencies

# Create application directory
WORKDIR /app

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 3: Production Image
# =============================================================================

FROM dependencies as production

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy application code
COPY main.py .
COPY kling_ai_client.py .
COPY templates/ templates/
COPY static/ static/
COPY sample_images/ sample_images/

# Copy scripts
COPY scripts/run_app.py scripts/

# Create required directories
RUN mkdir -p logs temp uploads && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/status || exit 1

# Default command
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# =============================================================================
# LABELS & METADATA
# =============================================================================

LABEL maintainer="AI Virtual Try-On Team" \
    version="1.0.0" \
    description="Professional AI-powered virtual clothing try-on application" \
    license="MIT"

# =============================================================================
# BUILD INSTRUCTIONS
# =============================================================================

# Build command:
# docker build -t ai-virtual-tryon .

# Run command:
# docker run -p 8000:8000 ai-virtual-tryon

# Run with environment variables:
# docker run -p 8000:8000 -e KLING_ACCESS_KEY=your_key -e KLING_SECRET_KEY=your_secret ai-virtual-tryon

# Run with volume mount for persistent data:
# docker run -p 8000:8000 -v $(pwd)/data:/app/data ai-virtual-tryon
