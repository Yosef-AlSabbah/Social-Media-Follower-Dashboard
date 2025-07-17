# Social-Media-Follower-Dashboard

A full-stack social media analytics dashboard built with React.js and Django. Displays real-time follower counts and growth trends across major platforms with clean, modern Arabic/RTL-friendly UI, Chart.js visualizations, and an async-ready REST API backed by PostgreSQL.

<div align="center">
  <img src="https://raw.githubusercontent.com/RSTAD/Social-Media-Follower-Dashboard/main/public/logo.svg" alt="Social Media Follower Dashboard Logo" width="150">
  <h1 align="center">Social Media Follower Dashboard</h1>
  <p align="center">
    A full-stack social media analytics dashboard built with React.js and Django. Displays real-time follower counts and growth trends across major platforms with clean, modern Arabic/RTL-friendly UI, Chart.js visualizations, and an async-ready REST API backed by PostgreSQL.
  </p>
  <div align="center">
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React Badge">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Badge">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL Badge">
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis Badge">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Badge">
    <img src="https://img.shields.io/badge/Nginx-269539?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx Badge">
  </div>
</div>

## ✨ Features

- **Real-Time Analytics**: Fetches and displays up-to-date follower counts.
- **Multi-Platform Support**: Tracks Facebook, Twitter, Instagram, and YouTube.
- **Growth Visualization**: Interactive charts showing follower trends over time.
- **Modern Tech Stack**: React.js frontend with a Django backend.
- **Clean, Responsive UI**: Arabic/RTL-friendly design that looks great on any device.
- **Async-Ready API**: Built for performance and scalability with Celery and Redis.
- **Containerized**: Fully containerized with Docker for easy deployment and scaling.

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RSTAD/Social-Media-Follower-Dashboard.git
   cd Social-Media-Follower-Dashboard
   ```

2. **Create a `.env` file** in the `Backend` directory by copying the example:
   ```bash
   cp Backend/.env.example Backend/.env
   ```
   Update the `.env` file with your desired settings.

3. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

4. **Open your browser** and navigate to `http://localhost`.

## 🐳 Docker Services

This project uses Docker to containerize all services for a consistent and reproducible environment.

- **`proxy`**: An Nginx reverse proxy that serves the frontend and routes API requests to the backend.
- **`backend`**: The Django application serving the REST API.
- **`frontend`**: The React.js application.
- **`db`**: A PostgreSQL database for data storage.
- **`redis`**: A Redis instance for caching and as a message broker for Celery.
- **`celery-worker`**: A Celery worker to process asynchronous tasks.
- **`celery-beat`**: A Celery beat scheduler for periodic tasks.

## API Endpoints

- `GET /api/followers`: Returns the latest follower counts for all platforms.
- `GET /api/followers/history`: Returns historical follower data for charts.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 📧 Contact

Rawad Al Furas - [Your Email] - [Your Project Link]

Project Link: [https://github.com/RSTAD/Social-Media-Follower-Dashboard](https://github.com/RSTAD/Social-Media-Follower-Dashboard)