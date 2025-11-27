# Simple in-memory storage for demo purposes
from typing import Dict
class Storage:
  def __init__(self):
    self._data: Dict[str, dict] = {}
  def upsert_vehicle(self, vid: str, payload: dict):
    self._data[vid] = payload
  def get_vehicle(self, vid: str):
    return self._data.get(vid)
  def list_vehicles(self):
    return list(self._data.values())
