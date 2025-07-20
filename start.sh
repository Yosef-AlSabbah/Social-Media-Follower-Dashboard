#!/bin/bash

# Function to wait for backend to be ready
wait_for_backend() {
    echo "Waiting for backend to be ready..."
    while ! curl -f http://localhost:8000/api/health/ 2>/dev/null; do
        echo "Backend not ready yet, waiting..."
        sleep 2
    done
    echo "Backend is ready!"
}

# Function to start backend
start_backend() {
    echo "Starting Django backend..."
    cd /app/Backend

    # Run migrations and setup
    uv run manage.py migrate --noinput
    uv run manage.py populate_fetch_scripts

    # Start Django server in background
    uv run manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!
    echo "Backend started with PID: $BACKEND_PID"
}

# Function to start frontend
start_frontend() {
    echo "Starting frontend..."
    cd /app/Frontend

    # Start frontend server
    bun run dev --host &
    FRONTEND_PID=$!
    echo "Frontend started with PID: $FRONTEND_PID"
}

# Function to start Celery worker
start_celery_worker() {
    echo "Starting Celery worker..."
    cd /app/Backend
    mkdir -p /app/Backend/logs
    chmod 755 /app/Backend/logs
    uv run celery -A core worker --loglevel=info &
    CELERY_WORKER_PID=$!
    echo "Celery worker started with PID: $CELERY_WORKER_PID"
}

# Function to start Celery beat
start_celery_beat() {
    echo "Starting Celery beat..."
    cd /app/Backend
    uv run celery -A core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
    CELERY_BEAT_PID=$!
    echo "Celery beat started with PID: $CELERY_BEAT_PID"
}

# Cleanup function
cleanup() {
    echo "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    kill $CELERY_WORKER_PID 2>/dev/null
    kill $CELERY_BEAT_PID 2>/dev/null
    exit 0
}

# Set up signal handlers for graceful shutdown
trap cleanup SIGTERM SIGINT

# Start services in order
start_backend
wait_for_backend
start_celery_worker
start_celery_beat
start_frontend

# Keep the script running and wait for all background processes
wait
