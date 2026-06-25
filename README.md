# PerfumeDecantBD

> **A luxury perfume e-commerce platform for Bangladesh — built with SvelteKit, FastAPI, and PostgreSQL.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Svelte](https://img.shields.io/badge/Frontend-SvelteKit-orange?style=flat-square)](https://kit.svelte.dev)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2016-336791?style=flat-square)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?style=flat-square)](https://www.docker.com)

---

## What is PerfumeDecantBD?

PerfumeDecantBD is a full-stack e-commerce web application tailored for the Bangladeshi perfume decant market. It allows customers to browse and purchase high-end perfume decants (small sample portions of luxury fragrances), while giving administrators tools to manage inventory, orders, and customers — all in one platform.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | SvelteKit + CSS |
| Backend | Python / FastAPI (async) |
| Database | PostgreSQL 16 |
| Auth | JWT (access + refresh tokens) |
| Email | SMTP (configurable) |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |

---

## Project Structure

```
PerfumeDecantsBD/
├── frontend/              # SvelteKit application
│   ├── src/               # Components, pages, stores
│   └── static/            # Public assets & images
├── backend/               # FastAPI application
│   └── src/               # API routes, models, services
├── uploads/               # Product image storage
├── .github/workflows/     # CI/CD pipelines
├── Dockerfile.backend     # Backend container definition
├── Dockerfile.frontend    # Frontend container definition
├── docker-compose.yml     # Multi-service orchestration
├── pyrightconfig.json     # Python type-checking config
├── .env.example           # Environment variable template
└── LICENSE
```

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/ArianThehunter/PerfumeDecantsBD.git
cd PerfumeDecantsBD
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and update the values. At minimum, change the passwords and `SECRET_KEY` before any deployment:

```env
# Database
POSTGRES_USER=perfume_admin
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=perfumedecantbd

# Backend
SECRET_KEY=your-super-secret-key-change-in-production

# Frontend
PUBLIC_SITE_NAME=PerfumeDecantBD
PUBLIC_SITE_DESCRIPTION=Luxury Perfume E-commerce Platform
```

### 3. Start all services

```bash
docker compose up -d
```

This brings up three containers:

| Container | Port | Description |
|---|---|---|
| `perfumedecantbd-db` | `5432` | PostgreSQL database |
| `perfumedecantbd-backend` | `8000` | FastAPI REST API |
| `perfumedecantbd-frontend` | `5173` | SvelteKit storefront |

### 4. Open the app

Navigate to **http://localhost:5173** in your browser.

The interactive API docs (Swagger UI) are available at **http://localhost:8000/docs**.

---

## Environment Variables Reference

| Variable | Default | Description |
|---|---|---|
| `POSTGRES_USER` | `perfume_admin` | Database username |
| `POSTGRES_PASSWORD` | `change_me_in_production` | Database password |
| `POSTGRES_DB` | `perfumedecantbd` | Database name |
| `POSTGRES_HOST` | `localhost` | Database host |
| `POSTGRES_PORT` | `5432` | Database port |
| `DATABASE_URL` | *(auto-constructed)* | Full async DB connection string |
| `SECRET_KEY` | `your-super-secret-key-...` | JWT signing secret |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifetime |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime |
| `CORS_ORIGINS` | `http://localhost:5173` | Allowed frontend origins |
| `ENVIRONMENT` | `development` | Runtime environment |
| `DEBUG` | `true` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Application log level |
| `PUBLIC_API_URL` | `http://localhost:8000/api` | Frontend API base URL |
| `PUBLIC_SITE_NAME` | `PerfumeDecantBD` | Site display name |
| `PUBLIC_SITE_DESCRIPTION` | `Luxury Perfume E-commerce Platform` | Site meta description |
| `SMTP_HOST` | `smtp.example.com` | Email server host |
| `SMTP_PORT` | `587` | Email server port |
| `SMTP_USER` | *(your email)* | Email account username |
| `SMTP_PASSWORD` | *(your email password)* | Email account password |
| `SMTP_FROM` | `noreply@perfumedecantbd.com` | Sender email address |
| `UPLOAD_DIR` | `./uploads` | Product image directory |
| `MAX_UPLOAD_SIZE_MB` | `10` | Maximum upload file size |

---

## Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Ensure PostgreSQL is running locally and your `.env` variables (especially `DATABASE_URL` with `POSTGRES_HOST=localhost`) are set before starting the backend.

---

## Key Features

- **E-commerce Storefront** — Browse perfume decant listings, view product details, and place orders.
- **Secure Authentication** — JWT-based login with access and refresh token rotation.
- **Admin Management** — Manage products, inventory, and customer orders through dedicated backend APIs.
- **Email Notifications** — SMTP-powered transactional emails for order confirmations and updates.
- **File Uploads** — Product image upload with configurable storage and size limits.
- **Async Backend** — FastAPI with `asyncpg` for high-performance, non-blocking database access.
- **Fully Containerized** — Separate Dockerfiles for backend and frontend, orchestrated with Docker Compose and a shared network bridge.
- **CI/CD Ready** — GitHub Actions workflows for automated testing and deployment.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "feat: add your feature"`.
4. Push and open a Pull Request.

Please ensure your code passes type checks (`pyright`) and any existing tests before submitting.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

© 2026 Md Readus Shalehin
