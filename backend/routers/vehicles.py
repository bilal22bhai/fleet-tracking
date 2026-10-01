from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from deps import current_user
from models import Vehicle, Location
from schemas import VehicleOut, LocationOut

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("", response_model=list[VehicleOut])
def my_vehicles(user=Depends(current_user), db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.company_id == user["company_id"]).all()

@router.get("/{vehicle_id}/history", response_model=list[LocationOut])
def history(
    vehicle_id: int,
    date_from: datetime | None = Query(None, alias="from"),
    date_to: datetime | None = Query(None, alias="to"),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle_id, Vehicle.company_id == user["company_id"])
        .first()
    )
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    q = db.query(Location).filter(Location.vehicle_id == vehicle_id)
    if date_from:
        q = q.filter(Location.timestamp >= date_from)
    if date_to:
        q = q.filter(Location.timestamp <= date_to)
    return q.order_by(Location.timestamp).limit(5000).all()
