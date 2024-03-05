from seamapi.types import (AbstractAccessGroupsAcs,AbstractSeam as Seam)
from typing import (Optional, Any)

class AccessGroupsAcs(AbstractAccessGroupsAcs):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
