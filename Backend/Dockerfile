# Use Python 3.13 slim image for production
FROM python:3.13-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_CACHE_DIR=/tmp/uv-cache

# Set work directory
WORKDIR /app

# Install system dependencies including Chrome and browser dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        netcat-openbsd \
        wget \
        gnupg \
        unzip \
        # Chrome dependencies
        libnss3 \
        libatk-bridge2.0-0 \
        libdrm2 \
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libgbm1 \
        libxss1 \
        libasound2 \
        libatspi2.0-0 \
        libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies as root
RUN uv sync --frozen --no-dev

# Create non-root user
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Copy project files with proper ownership
COPY --chown=django:django . .

# Create necessary directories with proper ownership
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && chown -R django:django /app/staticfiles /app/media /app/logs

# Copy entrypoint script
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-class", "sync", "--worker-connections", "1000", "--max-requests", "1000", "--max-requests-jitter", "50", "--timeout", "30", "--keep-alive", "2", "--access-logfile", "-", "--error-logfile", "-", "core.wsgi:application"]
