# Multi-stage build combining Python backend and Node.js frontend
FROM python:3.13-slim as backend-base

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    UV_CACHE_DIR=/tmp/uv-cache

# Install system dependencies including Chrome and Node.js
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        netcat-openbsd \
        git \
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

# Install Node.js and Bun
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g bun

# Install uv globally
RUN pip install uv

# Set the working directory for the application
WORKDIR /app

# Copy backend dependency files first for better caching
COPY Backend/pyproject.toml Backend/uv.lock ./Backend/

# Install Python dependencies
RUN cd Backend && uv sync --frozen --no-dev

# Copy frontend dependency files
COPY Frontend/package.json Frontend/bun.lockb* ./Frontend/

# Install frontend dependencies
RUN cd Frontend && bun install

# Create directories with proper permissions
RUN mkdir -p /app/Backend/staticfiles /app/Backend/media /app/Backend/logs \
    && chmod 755 /app/Backend/staticfiles /app/Backend/media /app/Backend/logs

# Copy the rest of the application code
COPY Backend/ ./Backend/
COPY Frontend/ ./Frontend/

# Build the frontend
RUN cd Frontend && bun run build

# Create startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports
EXPOSE 8000 3000

# Use the startup script as the entry point
CMD ["/start.sh"]
