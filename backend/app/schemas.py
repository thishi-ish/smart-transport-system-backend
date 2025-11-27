from pydantic import BaseModel, Field
from typing import Optional
class TelemetryIn(BaseModel):
  vehicle_id: str
  lat: float
  lon: float
  speed_m_s: Optional[float]
  heading: Optional[float]
  imu_ax: Optional[float]
  imu_ay: Optional[float]
  imu_az: Optional[float]
  bumps_per_min: Optional[int]
  bme_temp_c: Optional[float]
  bme_humidity: Optional[float]
  ldr_percent_drop: Optional[float]
  rain_analog: Optional[int]
  timestamp: Optional[str]

class VehicleOut(BaseModel):
  vehicle_id: str
  lat: float
  lon: float
  speed_m_s: Optional[float]
  heading: Optional[float]
  status: Optional[str]
  road_quality: Optional[str]
  fog_level: Optional[str]
  rain_level: Optional[str]
  eta_seconds: Optional[int]
