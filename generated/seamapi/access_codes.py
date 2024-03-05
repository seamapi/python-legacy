from seamapi.types import (AbstractAccessCodes,AbstractSeam as Seam,AccessCode,ActionAttempt)
from typing import (Optional, Any)

class AccessCodes(AbstractAccessCodes):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def create(self, device_id: Optional[Any] = None, name: Optional[Any] = None, starts_at: Optional[Any] = None, ends_at: Optional[Any] = None, code: Optional[Any] = None, sync: Optional[Any] = None, attempt_for_offline_device: Optional[Any] = None, common_code_key: Optional[Any] = None, prefer_native_scheduling: Optional[Any] = None, use_backup_access_code_pool: Optional[Any] = None, allow_external_modification: Optional[Any] = None, is_external_modification_allowed: Optional[Any] = None, use_offline_access_code: Optional[Any] = None, is_offline_access_code: Optional[Any] = None, is_one_time_use: Optional[Any] = None, max_time_rounding: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if name is not None:
      json_payload["name"] = name
    if starts_at is not None:
      json_payload["starts_at"] = starts_at
    if ends_at is not None:
      json_payload["ends_at"] = ends_at
    if code is not None:
      json_payload["code"] = code
    if sync is not None:
      json_payload["sync"] = sync
    if attempt_for_offline_device is not None:
      json_payload["attempt_for_offline_device"] = attempt_for_offline_device
    if common_code_key is not None:
      json_payload["common_code_key"] = common_code_key
    if prefer_native_scheduling is not None:
      json_payload["prefer_native_scheduling"] = prefer_native_scheduling
    if use_backup_access_code_pool is not None:
      json_payload["use_backup_access_code_pool"] = use_backup_access_code_pool
    if allow_external_modification is not None:
      json_payload["allow_external_modification"] = allow_external_modification
    if is_external_modification_allowed is not None:
      json_payload["is_external_modification_allowed"] = is_external_modification_allowed
    if use_offline_access_code is not None:
      json_payload["use_offline_access_code"] = use_offline_access_code
    if is_offline_access_code is not None:
      json_payload["is_offline_access_code"] = is_offline_access_code
    if is_one_time_use is not None:
      json_payload["is_one_time_use"] = is_one_time_use
    if max_time_rounding is not None:
      json_payload["max_time_rounding"] = max_time_rounding
    res = self.seam.make_request(
      "POST",
      "/access_codes/create",
      json=json_payload
    )
    return AccessCode.from_dict(res["access_code"])
  
  
  def create_multiple(self, device_ids: Optional[Any] = None, behavior_when_code_cannot_be_shared: Optional[Any] = None, name: Optional[Any] = None, starts_at: Optional[Any] = None, ends_at: Optional[Any] = None, code: Optional[Any] = None, attempt_for_offline_device: Optional[Any] = None, prefer_native_scheduling: Optional[Any] = None, use_backup_access_code_pool: Optional[Any] = None, allow_external_modification: Optional[Any] = None, is_external_modification_allowed: Optional[Any] = None, use_offline_access_code: Optional[Any] = None, is_offline_access_code: Optional[Any] = None, is_one_time_use: Optional[Any] = None, max_time_rounding: Optional[Any] = None):
    json_payload = {}
    if device_ids is not None:
      json_payload["device_ids"] = device_ids
    if behavior_when_code_cannot_be_shared is not None:
      json_payload["behavior_when_code_cannot_be_shared"] = behavior_when_code_cannot_be_shared
    if name is not None:
      json_payload["name"] = name
    if starts_at is not None:
      json_payload["starts_at"] = starts_at
    if ends_at is not None:
      json_payload["ends_at"] = ends_at
    if code is not None:
      json_payload["code"] = code
    if attempt_for_offline_device is not None:
      json_payload["attempt_for_offline_device"] = attempt_for_offline_device
    if prefer_native_scheduling is not None:
      json_payload["prefer_native_scheduling"] = prefer_native_scheduling
    if use_backup_access_code_pool is not None:
      json_payload["use_backup_access_code_pool"] = use_backup_access_code_pool
    if allow_external_modification is not None:
      json_payload["allow_external_modification"] = allow_external_modification
    if is_external_modification_allowed is not None:
      json_payload["is_external_modification_allowed"] = is_external_modification_allowed
    if use_offline_access_code is not None:
      json_payload["use_offline_access_code"] = use_offline_access_code
    if is_offline_access_code is not None:
      json_payload["is_offline_access_code"] = is_offline_access_code
    if is_one_time_use is not None:
      json_payload["is_one_time_use"] = is_one_time_use
    if max_time_rounding is not None:
      json_payload["max_time_rounding"] = max_time_rounding
    res = self.seam.make_request(
      "POST",
      "/access_codes/create_multiple",
      json=json_payload
    )
    return [AccessCode.from_dict(item) for item in res["access_codes"]]
  
  
  def delete(self, device_id: Optional[Any] = None, access_code_id: Optional[Any] = None, sync: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if access_code_id is not None:
      json_payload["access_code_id"] = access_code_id
    if sync is not None:
      json_payload["sync"] = sync
    res = self.seam.make_request(
      "POST",
      "/access_codes/delete",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])
  
  
  def generate_code(self, device_id: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    res = self.seam.make_request(
      "POST",
      "/access_codes/generate_code",
      json=json_payload
    )
    return AccessCode.from_dict(res["generated_code"])
  
  
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
      "/access_codes/get",
      json=json_payload
    )
    return AccessCode.from_dict(res["access_code"])
  
  
  def list(self, device_id: Optional[Any] = None, access_code_ids: Optional[Any] = None, user_identifier_key: Optional[Any] = None):
    json_payload = {}
    if device_id is not None:
      json_payload["device_id"] = device_id
    if access_code_ids is not None:
      json_payload["access_code_ids"] = access_code_ids
    if user_identifier_key is not None:
      json_payload["user_identifier_key"] = user_identifier_key
    res = self.seam.make_request(
      "POST",
      "/access_codes/list",
      json=json_payload
    )
    return [AccessCode.from_dict(item) for item in res["access_codes"]]
  
  
  def pull_backup_access_code(self, access_code_id: Optional[Any] = None):
    json_payload = {}
    if access_code_id is not None:
      json_payload["access_code_id"] = access_code_id
    res = self.seam.make_request(
      "POST",
      "/access_codes/pull_backup_access_code",
      json=json_payload
    )
    return AccessCode.from_dict(res["backup_access_code"])
  
  
  def update(self, name: Optional[Any] = None, starts_at: Optional[Any] = None, ends_at: Optional[Any] = None, code: Optional[Any] = None, sync: Optional[Any] = None, attempt_for_offline_device: Optional[Any] = None, prefer_native_scheduling: Optional[Any] = None, use_backup_access_code_pool: Optional[Any] = None, allow_external_modification: Optional[Any] = None, is_external_modification_allowed: Optional[Any] = None, use_offline_access_code: Optional[Any] = None, is_offline_access_code: Optional[Any] = None, is_one_time_use: Optional[Any] = None, max_time_rounding: Optional[Any] = None, access_code_id: Optional[Any] = None, device_id: Optional[Any] = None, type: Optional[Any] = None, is_managed: Optional[Any] = None):
    json_payload = {}
    if name is not None:
      json_payload["name"] = name
    if starts_at is not None:
      json_payload["starts_at"] = starts_at
    if ends_at is not None:
      json_payload["ends_at"] = ends_at
    if code is not None:
      json_payload["code"] = code
    if sync is not None:
      json_payload["sync"] = sync
    if attempt_for_offline_device is not None:
      json_payload["attempt_for_offline_device"] = attempt_for_offline_device
    if prefer_native_scheduling is not None:
      json_payload["prefer_native_scheduling"] = prefer_native_scheduling
    if use_backup_access_code_pool is not None:
      json_payload["use_backup_access_code_pool"] = use_backup_access_code_pool
    if allow_external_modification is not None:
      json_payload["allow_external_modification"] = allow_external_modification
    if is_external_modification_allowed is not None:
      json_payload["is_external_modification_allowed"] = is_external_modification_allowed
    if use_offline_access_code is not None:
      json_payload["use_offline_access_code"] = use_offline_access_code
    if is_offline_access_code is not None:
      json_payload["is_offline_access_code"] = is_offline_access_code
    if is_one_time_use is not None:
      json_payload["is_one_time_use"] = is_one_time_use
    if max_time_rounding is not None:
      json_payload["max_time_rounding"] = max_time_rounding
    if access_code_id is not None:
      json_payload["access_code_id"] = access_code_id
    if device_id is not None:
      json_payload["device_id"] = device_id
    if type is not None:
      json_payload["type"] = type
    if is_managed is not None:
      json_payload["is_managed"] = is_managed
    res = self.seam.make_request(
      "POST",
      "/access_codes/update",
      json=json_payload
    )
    return ActionAttempt.from_dict(res["action_attempt"])