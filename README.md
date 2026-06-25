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

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

© 2026 Md Readus Shalehin
