# EngineerOS

EngineerOS is a learning operating system for software engineers.

## Sprint 1 Status
In progress.

## Local Development (Sprint 1 baseline)
- Frontend: React + TypeScript
- Backend: FastAPI (Python 3.12)
- Database: PostgreSQL 16

## Project Structure
- frontend
- backend
- database
- docs
- scripts

## Run Locally (Sprint 1)

### 1) Start Frontend
```bash
cd frontend
npm install
npm run dev
## Auth API Quick Test (Sprint 2)

### Register
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"password123","full_name":"Alice Doe"}'