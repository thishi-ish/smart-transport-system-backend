from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas import TelemetryIn, VehicleOut
from app.storage import Storage
from app.eta import compute_eta
app = FastAPI(title="Smart Transport Backend")
store = Storage()
@app.post('/ingest', response_model=dict)
async def ingest(telemetry: TelemetryIn):
# Validate and store
vehicle_id = telemetry.vehicle_id
data = telemetry.dict()
data['received_at'] = datetime.utcnow().isoformat()
store.upsert_vehicle(vehicle_id, data)
return {"status": "ok"}
@app.get('/vehicles', response_model=List[VehicleOut])
async def list_vehicles():
items = store.list_vehicles()
# attach ETA computed
out = []
for v in items:
v_copy = v.copy()
try:
v_copy['eta_seconds'] = compute_eta(v_copy)
except Exception:
v_copy['eta_seconds'] = None
out.append(v_copy)
return out
@app.get('/vehicles/{vehicle_id}', response_model=VehicleOut)
async def get_vehicle(vehicle_id: str):
v = store.get_vehicle(vehicle_id)
if not v:
raise HTTPException(status_code=404, detail='Not found')
v['eta_seconds'] = compute_eta(v)
return v
