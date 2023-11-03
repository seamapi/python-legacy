from seamapi.types import (AbstractClientSessions,AbstractSeam as Seam,ClientSession)
from typing import (Optional, Any)

class ClientSessions(AbstractClientSessions):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def create(self, user_identifier_key: Optional[Any] = None, connect_webview_ids: Optional[Any] = None, connected_account_ids: Optional[Any] = None):
    json_payload = {}
    if user_identifier_key is not None:
      json_payload["user_identifier_key"] = user_identifier_key
    if connect_webview_ids is not None:
      json_payload["connect_webview_ids"] = connect_webview_ids
    if connected_account_ids is not None:
      json_payload["connected_account_ids"] = connected_account_ids
    res = self.seam.make_request(
      "POST",
      "/client_sessions/create",
      json=json_payload
    )
    return ClientSession.from_dict(res["client_session"])
  
  
  def get(self, client_session_id: Any, user_identifier_key: Optional[Any] = None):
    json_payload = {}
    if client_session_id is not None:
      json_payload["client_session_id"] = client_session_id
    if user_identifier_key is not None:
      json_payload["user_identifier_key"] = user_identifier_key
    res = self.seam.make_request(
      "POST",
      "/client_sessions/get",
      json=json_payload
    )
    return ClientSession.from_dict(res["client_session"])
  
  
  def get_or_create(self, user_identifier_key: Optional[Any] = None, connect_webview_ids: Optional[Any] = None, connected_account_ids: Optional[Any] = None):
    json_payload = {}
    if user_identifier_key is not None:
      json_payload["user_identifier_key"] = user_identifier_key
    if connect_webview_ids is not None:
      json_payload["connect_webview_ids"] = connect_webview_ids
    if connected_account_ids is not None:
      json_payload["connected_account_ids"] = connected_account_ids
    res = self.seam.make_request(
      "POST",
      "/client_sessions/get_or_create",
      json=json_payload
    )
    return ClientSession.from_dict(res["client_session"])
  
  
  def list(self, client_session_id: Optional[Any] = None, user_identifier_key: Optional[Any] = None, connect_webview_id: Optional[Any] = None, without_user_identifier_key: Optional[Any] = None):
    json_payload = {}
    if client_session_id is not None:
      json_payload["client_session_id"] = client_session_id
    if user_identifier_key is not None:
      json_payload["user_identifier_key"] = user_identifier_key
    if connect_webview_id is not None:
      json_payload["connect_webview_id"] = connect_webview_id
    if without_user_identifier_key is not None:
      json_payload["without_user_identifier_key"] = without_user_identifier_key
    res = self.seam.make_request(
      "POST",
      "/client_sessions/list",
      json=json_payload
    )
    return [ClientSession.from_dict(item) for item in res["client_sessions"]]