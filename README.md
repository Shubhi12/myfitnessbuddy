# My Fitness Buddy

A production-ready platform for gated community residents to find fitness partners and book community amenities.

## Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, MySQL 8, JWT, Redis, Celery |
| **Mobile** | Flutter, Riverpod, GoRouter, Dio, Material 3 |
| **Admin** | React 19, TypeScript, Vite, Material UI, React Query |
| **Deployment** | Docker Compose, Nginx, GitHub Actions |

## Quick Start

```bash
# Clone and configure
cp .env.example .env

# Start all services
make up

# Run migrations
make migrate

# Seed sample data
make seed
```

**Endpoints:**
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Admin: http://localhost:5173
- Nginx gateway: http://localhost:80

## Project Structure

```
├── backend/     # FastAPI · Clean Architecture
├── mobile/      # Flutter mobile app
├── admin/       # React admin panel
├── deploy/      # Nginx & Docker scripts
└── docs/        # Architecture documentation
```

## Development

```bash
# Backend tests
make test

# Admin dev server
make admin-dev

# Flutter tests
make mobile-test
```

## Architecture

The backend follows **Clean Architecture** with four layers:

- **Domain** — entities, value objects, repository interfaces
- **Application** — services, DTOs, use cases
- **Infrastructure** — SQLAlchemy models, Redis, Celery
- **Presentation** — FastAPI routes, Pydantic schemas

## License

Proprietary — All rights reserved.
