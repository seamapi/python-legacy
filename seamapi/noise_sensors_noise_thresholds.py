from seamapi.types import (AbstractNoiseThresholdsNoiseSensors,AbstractSeam as Seam,ActionAttempt,NoiseThreshold)
from typing import (Optional, Any)

class NoiseThresholdsNoiseSensors(AbstractNoiseThresholdsNoiseSensors):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def create(self, device_id: Optional[Any] = None, sync: Optional[Any] = None, name: Optional[Any] = None, starts_daily_at: Optional[Any] = None, ends_daily_at: Optional[Any] = None, noise_threshold_decibels: Optional[Any] = None, noise_threshold_nrs: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if sync is not None:
      json_payload["sync"] = sync
    if name is not None:
      json_payload["name"] = name
    if starts_daily_at is not None:
      json_payload["starts_daily_at"] = starts_daily_at
    if ends_daily_at is not None:
      json_payload["ends_daily_at"] = ends_daily_at
    if noise_threshold_decibels is not None:
      json_payload["noise_threshold_decibels"] = noise_threshold_decibels
    if noise_threshold_nrs is not None:
      json_payload["noise_threshold_nrs"] = noise_threshold_nrs
    res = self.seam.make_request(
      "POST",
      "/noise_sensors/noise_thresholds/create",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])
  
  
  def delete(self, noise_threshold_id: Optional[Any] = None, device_id: Optional[Any] = None, sync: Optional[Any] = None):
    json_payload = {}
    if noise_threshold_id is not None:
      json_payload["noise_threshold_id"] = noise_threshold_id
    if device_id is not None:
      json_payload["device_id"] = device_id
    if sync is not None:
      json_payload["sync"] = sync
    res = self.seam.make_request(
      "POST",
      "/noise_sensors/noise_thresholds/delete",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])
  
  
  def get(self, noise_threshold_id: Any):
    json_payload = {}
    if noise_threshold_id is not None:
      json_payload["noise_threshold_id"] = noise_threshold_id
    res = self.seam.make_request(
      "POST",
      "/noise_sensors/noise_thresholds/get",
      json=json_payload
    )
    return NoiseThreshold.from_dict(res["noise_threshold"])
  
  
  def list(self, device_id: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    res = self.seam.make_request(
      "POST",
      "/noise_sensors/noise_thresholds/list",
      json=json_payload
    )
    return [NoiseThreshold.from_dict(item) for item in res["noise_thresholds"]]
  
  
  def update(self, noise_threshold_id: Optional[Any] = None, device_id: Optional[Any] = None, sync: Optional[Any] = None, name: Optional[Any] = None, starts_daily_at: Optional[Any] = None, ends_daily_at: Optional[Any] = None, noise_threshold_decibels: Optional[Any] = None, noise_threshold_nrs: Optional[Any] = None):
    json_payload = {}
    if noise_threshold_id is not None:
      json_payload["noise_threshold_id"] = noise_threshold_id
    if device_id is not None:
      json_payload["device_id"] = device_id
    if sync is not None:
      json_payload["sync"] = sync
    if name is not None:
      json_payload["name"] = name
    if starts_daily_at is not None:
      json_payload["starts_daily_at"] = starts_daily_at
    if ends_daily_at is not None:
      json_payload["ends_daily_at"] = ends_daily_at
    if noise_threshold_decibels is not None:
      json_payload["noise_threshold_decibels"] = noise_threshold_decibels
    if noise_threshold_nrs is not None:
      json_payload["noise_threshold_nrs"] = noise_threshold_nrs
    res = self.seam.make_request(
      "POST",
      "/noise_sensors/noise_thresholds/update",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])