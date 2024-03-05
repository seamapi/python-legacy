from seamapi.types import (AbstractUsersAcs,AbstractSeam as Seam)
from typing import (Optional, Any)

class UsersAcs(AbstractUsersAcs):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
