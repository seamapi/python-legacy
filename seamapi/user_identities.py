from seamapi.types import (AbstractUserIdentities,AbstractSeam as Seam)
from typing import (Optional, Any)

class UserIdentities(AbstractUserIdentities):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
