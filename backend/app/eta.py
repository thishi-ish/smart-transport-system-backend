# Implements ETA logic from your spec. Returns ETA in seconds (approx) or
None if not computable.
import math
def dew_point(T, RH):
# Use the simplified dewpoint formula from spec
return T - ((100 - RH) / 5.0)
def fog_level_from(bme_temp_c, bme_humidity, ldr_drop):
if bme_temp_c is None or bme_humidity is None:
return 'clear'
dp = dew_point(bme_temp_c, bme_humidity)
if bme_humidity > 90 and abs(bme_temp_c - dp) < 2 and (ldr_drop or 0) >
30:
return 'heavy'
if bme_humidity > 80 and abs(bme_temp_c - dp) < 4:
return 'light'
return 'clear'
def rain_level_from(rain_analog):
if rain_analog is None:
return 'none'
if 0 <= rain_analog <= 300:
return 'heavy'
if 301 <= rain_analog <= 700:
return 'light'
return 'none'
def road_from(bumps_per_min, imu_az, imu_ax):
if bumps_per_min is not None and bumps_per_min > 5:
return 'bad'
# fallback to imu heuristics
if imu_az is not None and abs(imu_az) > 15:
return 'bad'
return 'good'
def compute_eta(vehicle_record: dict) -> int:
# naive ETA: assume destination is a fixed point for demo (replace in
real app)
4
# For demo, if speed present use 5km ahead as remaining distance
base_distance_m = 5000 # placeholder 5km
speed = vehicle_record.get('speed_m_s') or 10.0
if speed <= 0.1:
return None
base_eta = base_distance_m / speed # seconds
# modifiers
eta_multiplier = 1.0
# road
road = road_from(vehicle_record.get('bumps_per_min'),
vehicle_record.get('imu_az'), vehicle_record.get('imu_ax'))
if road == 'bad':
eta_multiplier *= 1.10
# fog
fog = fog_level_from(vehicle_record.get('bme_temp_c'),
vehicle_record.get('bme_humidity'), vehicle_record.get('ldr_percent_drop'))
if fog == 'light':
eta_multiplier *= 1.15
if fog == 'heavy':
eta_multiplier *= 1.35
# rain
rain = rain_level_from(vehicle_record.get('rain_analog'))
if rain == 'light':
eta_multiplier *= 1.10
if rain == 'heavy':
eta_multiplier *= 1.25
final_eta = base_eta * eta_multiplier
return int(final_eta)
