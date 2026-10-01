from datetime import datetime
from pydantic import BaseModel

class LoginIn(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class VehicleOut(BaseModel):
    id: int
    device_id: str
    plate_number: str
    name: str
    last_lat: float | None
    last_lng: float | None
    last_speed: float | None
    last_seen: datetime | None
    model_config = {"from_attributes": True}

class LocationOut(BaseModel):
    lat: float
    lng: float
    speed: float
    timestamp: datetime
    model_config = {"from_attributes": True}
