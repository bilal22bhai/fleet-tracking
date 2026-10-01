import asyncio
from datetime import datetime, timezone
import httpx
from config import PROVIDER_URL, PROVIDER_KEY, POLL_SECONDS
from database import SessionLocal
from models import Vehicle, Location

def save_positions(items: list[dict]):
    db = SessionLocal()
    try:
        vehicles = {v.device_id: v for v in db.query(Vehicle).all()}
        for p in items:
            v = vehicles.get(p["device_id"])
            if not v:
                continue
            ts = datetime.fromtimestamp(p["timestamp"], tz=timezone.utc).replace(tzinfo=None)
            v.last_lat, v.last_lng = p["lat"], p["lng"]
            v.last_speed, v.last_seen = p["speed"], ts
            db.add(Location(vehicle_id=v.id, lat=p["lat"], lng=p["lng"],
                            speed=p["speed"], timestamp=ts))
        db.commit()
    finally:
        db.close()

async def poll_provider():
    async with httpx.AsyncClient(timeout=10) as client:
        while True:
            try:
                r = await client.get(PROVIDER_URL, headers={"x-api-key": PROVIDER_KEY})
                r.raise_for_status()
                save_positions(r.json())
            except Exception as e:
                print("Provider error:", e)
            await asyncio.sleep(POLL_SECONDS)
