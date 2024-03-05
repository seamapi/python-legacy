from seamapi.types import (AbstractSystemsAcs,AbstractSeam as Seam)
from typing import (Optional, Any)

class SystemsAcs(AbstractSystemsAcs):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
