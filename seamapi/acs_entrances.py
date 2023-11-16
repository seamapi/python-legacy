from seamapi.types import (AbstractEntrancesAcs,AbstractSeam as Seam)
from typing import (Optional, Any)

class EntrancesAcs(AbstractEntrancesAcs):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
