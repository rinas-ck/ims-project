from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 Ingest signal
@app.post("/signal")
def ingest_signal(component: str, db: Session = Depends(get_db)):
    incident = models.Incident(component=component)
    db.add(incident)
    db.commit()
    return {"message": "Incident created"}

# 📊 Get incidents
@app.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(models.Incident).all()

# 🔄 Update status
@app.put("/incident/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Not found")

    # 🔥 Mandatory RCA rule
    if status == "CLOSED" and not incident.rca:
        raise HTTPException(status_code=400, detail="RCA required")

    incident.status = status
    db.commit()
    return {"message": "Updated"}

# 🧠 Add RCA
@app.post("/incident/{id}/rca")
def add_rca(id: int, rca: str, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == id).first()
    incident.rca = rca
    db.commit()
    return {"message": "RCA added"}
