from seamapi.types import (AbstractLocks,AbstractSeam as Seam,ActionAttempt)
from typing import (Optional, Any)

class Locks(AbstractLocks):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def lock_door(self, device_id: Optional[Any] = None, sync: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if sync is not None:
      json_payload["sync"] = sync
    res = self.seam.make_request(
      "POST",
      "/locks/lock_door",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])
  
  
  def unlock_door(self, device_id: Optional[Any] = None, sync: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if sync is not None:
      json_payload["sync"] = sync
    res = self.seam.make_request(
      "POST",
      "/locks/unlock_door",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])