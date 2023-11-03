from seamapi.types import (AbstractUnmanagedAccessCodes,AbstractSeam as Seam,ActionAttempt,UnmanagedAccessCode)
from typing import (Optional, Any)

class UnmanagedAccessCodes(AbstractUnmanagedAccessCodes):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def delete(self, access_code_id: Optional[Any] = None, sync: Optional[Any] = None):
    json_payload = {}
    if access_code_id is not None:
      json_payload["access_code_id"] = access_code_id
    if sync is not None:
      json_payload["sync"] = sync
    res = self.seam.make_request(
      "POST",
      "/access_codes/unmanaged/delete",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])
  
  
  def get(self, access_code_id: Any, device_id: Optional[Any] = None, code: Optional[Any] = None):
    json_payload = {}
    if access_code_id is not None:
      json_payload["access_code_id"] = access_code_id
    if device_id is not None:
      json_payload["device_id"] = device_id
    if code is not None:
      json_payload["code"] = code
    res = self.seam.make_request(
      "POST",
      "/access_codes/unmanaged/get",
      json=json_payload
    )
    return UnmanagedAccessCode.from_dict(res["access_code"])
  
  
  def list(self, device_id: Optional[Any] = None, user_identifier_key: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if user_identifier_key is not None:
      json_payload["user_identifier_key"] = user_identifier_key
    res = self.seam.make_request(
      "POST",
      "/access_codes/unmanaged/list",
      json=json_payload
    )
    return [UnmanagedAccessCode.from_dict(item) for item in res["access_codes"]]