# Phase II: Full-Stack Web Application Architecture

## Overview
Phase II transforms the Phase I CLI application into a full-stack web application for managing tickets with a modern frontend and RESTful backend API.

## Tech Stack

### Backend
- **Framework**: FastAPI
  - High-performance async framework
  - Automatic API documentation (OpenAPI/Swagger)
  - Built-in data validation with Pydantic
  - Type hints and IDE support

- **Database**: Neon Serverless PostgreSQL
  - Serverless PostgreSQL database
  - Auto-scaling with no infrastructure management
  - Secure connection via connection pooling
  - Compatible with existing PostgreSQL tooling

- **Database ORM**: SQLAlchemy (async)
  - Async SQLAlchemy for database operations
  - Migration support with Alembic
  - Compatible with Pydantic models

### Frontend
- **Framework**: Next.js 14+ (App Router)
  - React framework with SSR/SSG capabilities
  - App Router for modern routing
  - Built-in API routes
  - TypeScript support out of the box

- **UI Library**: shadcn/ui + Tailwind CSS
  - Beautiful, accessible components
  - Fully customizable
  - Dark mode support
  - Excellent DX with components copy-paste

- **State Management**: React Context / Zustand
  - Simple state management for ticket CRUD
  - Server state caching with SWR or TanStack Query
  - Optimistic updates

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐│
│  │ Ticket List   │  │ Ticket Form  │  │ Dashboard││
│  └──────────────┘  └──────────────┘  └──────────┘│
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/JSON (REST API)
┌────────────────────┴────────────────────────────────────────┐
│              Backend (FastAPI)                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐│
│  │  API Routes│  │  Pydantic  │  │  Auth      ││
│  │  /tickets  │  │  Schemas   │  │  (Phase III)││
│  └────────────┘  └────────────┘  └────────────┘│
└────────────────────┬────────────────────────────────────────┘
                     │
              Neon Serverless PostgreSQL
│  ┌──────────────────────────┐  │
│  │   tickets table         │  │
│  │   - id                │  │
│  │   - title             │  │
│  │   - priority          │  │
│  │   - status            │  │
│  │   - created_at       │  │
│  │   - updated_at       │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
```

## Database Schema

### tickets table
```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    priority VARCHAR(10) NOT NULL CHECK (priority IN ('LOW', 'MED', 'HIGH')),
    status VARCHAR(10) NOT NULL CHECK (status IN ('BACKLOG', 'DONE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Project Structure

```
todo-phase2/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py       # FastAPI application
│   │   ├── config.py     # Database configuration
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── crud.py       # Database operations
│   │   └── deps.py      # Dependencies
│   ├── tests/            # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── alembic/         # Database migrations
├── frontend/            # Next.js frontend
│   ├── app/
│   │   ├── page.tsx     # Home page
│   │   ├── tickets/      # Tickets pages
│   │   ├── components/   # React components
│   │   └── lib/         # Utilities and API clients
│   ├── public/
│   ├── components/       # shadcn/ui components
│   └── package.json
└── .specify/
    └── web/
        └── architecture.md
```

## API Endpoints

### Tickets API
- `GET /api/tickets` - List all tickets
- `GET /api/tickets/{id}` - Get single ticket
- `POST /api/tickets` - Create new ticket
- `PUT /api/tickets/{id}` - Update ticket
- `DELETE /api/tickets/{id}` - Delete ticket
- `PATCH /api/tickets/{id}/status` - Update ticket status
- `PATCH /api/tickets/{id}/priority` - Update ticket priority

### Query Parameters
- `?status=BACKLOG` - Filter by status
- `?priority=HIGH` - Filter by priority
- `?sort=created_at&order=desc` - Sorting

## Frontend Pages

### Main Pages
1. **Home/Dashboard** (`/`)
   - Statistics overview
   - Recent tickets
   - Quick actions

2. **Tickets List** (`/tickets`)
   - Table/grid view of all tickets
   - Filter by status/priority
   - Search functionality
   - Pagination

3. **Ticket Details** (`/tickets/[id]`)
   - View ticket details
   - Edit/delete actions
   - History/timeline

4. **Create Ticket** (`/tickets/new`)
   - Form to create new ticket
   - Validation
   - Success/error states

## Phase II Features

### Backend
- [ ] FastAPI application setup
- [ ] SQLAlchemy models with Neon PostgreSQL
- [ ] CRUD API endpoints
- [ ] Request/response schemas
- [ ] Database migrations with Alembic
- [ ] CORS configuration
- [ ] Error handling
- [ ] API documentation (Swagger UI)

### Frontend
- [ ] Next.js 14+ project setup with App Router
- [ ] shadcn/ui components setup
- [ ] Tickets list page with table
- [ ] Create ticket form
- [ ] Update ticket modal/page
- [ ] Delete confirmation
- [ ] Status badge components
- [ ] Priority badge components
- [ ] Loading states
- [ ] Error handling
- [ ] Dark mode support

### Integration
- [ ] API client for backend calls
- [ ] Form validation (zod)
- [ ] Optimistic updates
- [ ] Error toast notifications
- [ ] Real-time updates (optional: WebSockets)

## Migration Path from Phase I

1. **Keep Phase I CLI as is** - Useful for automation and scripts
2. **Backend conversion**
   - Move `src/` to `backend/app/`
   - Convert in-memory storage to SQLAlchemy
   - Wrap logic in FastAPI routes
   - Add Pydantic request/response schemas
3. **Frontend creation**
   - Initialize Next.js project
   - Create pages for all CRUD operations
   - Connect to backend API
   - Style with shadcn/ui + Tailwind

## Next Steps

1. Setup backend FastAPI with Neon PostgreSQL
2. Create SQLAlchemy models matching Phase I tickets
3. Implement REST API endpoints
4. Initialize Next.js frontend with shadcn/ui
5. Build frontend pages and components
6. Integrate frontend with backend API
7. Add testing for both backend and frontend
8. Deploy to production (Vercel for frontend, Railway/Render for backend)

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@ep-xxx.aws.neon.tech/neondb?sslmode=require
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

**Status**: Phase II Planning Complete
**Next**: Begin Backend FastAPI Implementation
