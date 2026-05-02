from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models
import datetime


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 Ingest signal
from datetime import datetime, timedelta

@app.post("/signal")
def ingest_signal(component: str, db: Session = Depends(get_db)):

    last_incident = db.query(models.Incident)\
        .filter(models.Incident.component == component)\
        .order_by(models.Incident.id.desc())\
        .first()

    if last_incident:
        time_diff = datetime.utcnow() - last_incident.created_at
        if time_diff < timedelta(seconds=10):
            return {"message": "Duplicate signal ignored (debounced)"}

    incident = models.Incident(component=component)
    db.add(incident)
    db.commit()

    return {"message": "Incident created"}

# 🔄 Update status
@app.put("/incident/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Not found")

    # RCA validation
    if status == "CLOSED" and not incident.rca:
        raise HTTPException(status_code=400, detail="RCA required")

    incident.status = status

    # Save close time
    if status == "CLOSED":
        incident.closed_at = datetime.datetime.utcnow()

    db.commit()

    return {"message": "Updated"}

# 🧠 Add RCA
@app.post("/incident/{id}/rca")
def add_rca(id: int, rca: str, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == id).first()
    incident.rca = rca
    db.commit()
    return {"message": "RCA added"}
# taking
@app.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(models.Incident).all()

    if not incident.closed_at:
        return {"message": "Incident not closed yet"}

    mttr = incident.closed_at - incident.created_at
    return {"MTTR": str(mttr)}