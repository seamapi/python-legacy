from seamapi.types import (AbstractActionAttempts,AbstractSeam as Seam,ActionAttempt)
from typing import (Optional, Any)

class ActionAttempts(AbstractActionAttempts):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def get(self, action_attempt_id: Any):
    json_payload = {}
    if action_attempt_id is not None:
      json_payload["action_attempt_id"] = action_attempt_id
    res = self.seam.make_request(
      "POST",
      "/action_attempts/get",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])
  
  
  def list(self, action_attempt_ids: Optional[Any] = None):
    json_payload = {}
    if action_attempt_ids is not None:
      json_payload["action_attempt_ids"] = action_attempt_ids
    res = self.seam.make_request(
      "POST",
      "/action_attempts/list",
      json=json_payload
    )
    return [ActionAttempt.from_dict(item) for item in res["action_attempts"]]