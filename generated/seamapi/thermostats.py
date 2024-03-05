from seamapi.types import (AbstractThermostats,AbstractSeam as Seam,Device)
from typing import (Optional, Any)

class Thermostats(AbstractThermostats):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def get(self, device_id: Optional[Any] = None, name: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if name is not None:
      json_payload["name"] = name
    res = self.seam.make_request(
      "POST",
      "/thermostats/get",
      json=json_payload
    )
    return Device.from_dict(res["thermostat"])
  
  
  def list(self, connected_account_id: Optional[Any] = None, connected_account_ids: Optional[Any] = None, connect_webview_id: Optional[Any] = None, device_types: Optional[Any] = None, manufacturer: Optional[Any] = None, device_ids: Optional[Any] = None, limit: Optional[Any] = None, created_before: Optional[Any] = None, user_identifier_key: Optional[Any] = None):
    json_payload = {}
    if connected_account_id is not None:
      json_payload["connected_account_id"] = connected_account_id
    if connected_account_ids is not None:
      json_payload["connected_account_ids"] = connected_account_ids
    if connect_webview_id is not None:
      json_payload["connect_webview_id"] = connect_webview_id
    if device_types is not None:
      json_payload["device_types"] = device_types
    if manufacturer is not None:
      json_payload["manufacturer"] = manufacturer
    if device_ids is not None:
      json_payload["device_ids"] = device_ids
    if limit is not None:
      json_payload["limit"] = limit
    if created_before is not None:
      json_payload["created_before"] = created_before
    if user_identifier_key is not None:
      json_payload["user_identifier_key"] = user_identifier_key
    res = self.seam.make_request(
      "POST",
      "/thermostats/list",
      json=json_payload
    )
    return [Device.from_dict(item) for item in res["thermostats"]]