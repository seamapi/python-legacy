from seamapi.types import (AbstractWorkspaces,AbstractSeam as Seam,Workspace)
from typing import (Optional, Any)

class Workspaces(AbstractWorkspaces):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam

  
  
  def get(self, ):
    json_payload = {}
    res = self.seam.make_request(
      "POST",
      "/workspaces/get",
      json=json_payload
    )
    return Workspace.from_dict(res["workspace"])