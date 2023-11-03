from seamapi.types import (AbstractConnectedAccounts,AbstractSeam as Seam,ConnectedAccount)
from typing import (Optional, Any)

class ConnectedAccounts(AbstractConnectedAccounts):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def get(self, connected_account_id: Any, email: Optional[Any] = None):
    json_payload = {}
    if connected_account_id is not None:
      json_payload["connected_account_id"] = connected_account_id
    if email is not None:
      json_payload["email"] = email
    res = self.seam.make_request(
      "POST",
      "/connected_accounts/get",
      json=json_payload
    )
    return ConnectedAccount.from_dict(res["connected_account"])
  
  
  def list(self, ):
    json_payload = {}
    res = self.seam.make_request(
      "POST",
      "/connected_accounts/list",
      json=json_payload
    )
    return [ConnectedAccount.from_dict(item) for item in res["connected_accounts"]]