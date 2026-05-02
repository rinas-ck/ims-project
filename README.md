# Incident Management System (IMS)

## Features
- Signal ingestion API
- Incident dashboard
- Severity mapping (P0/P1/P2)
- RCA validation before closure
- Debouncing logic
- MTTR calculation
- FastAPI backend
- Simple frontend dashboard

## Tech Stack
- FastAPI
- SQLite
- HTML/CSS/JavaScript

## Run Instructions

### Backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

### Frontend
Open frontend/index.html using Live Server

## APIs
- POST /signal
- GET /incidents
- PUT /incident/{id}/status
- POST /incident/{id}/rca

