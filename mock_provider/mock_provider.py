import random, time
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Mock Tracking Provider")
API_KEY = "demo-key-123"

cars = [
    {"device_id": f"DEV{i:03d}", "plate": f"LEA-{1000+i}",
     "lat": 31.52 + random.uniform(-0.05, 0.05),
     "lng": 74.35 + random.uniform(-0.05, 0.05)}
    for i in range(1, 21)
]

@app.get("/api/devices/positions")
def positions(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    out = []
    for c in cars:
        c["lat"] += random.uniform(-0.001, 0.001)
        c["lng"] += random.uniform(-0.001, 0.001)
        out.append({**c, "speed": round(random.uniform(0, 80), 1),
                    "timestamp": int(time.time())})
    return out
