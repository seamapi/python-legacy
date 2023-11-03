from seamapi.types import (AbstractServiceHealth,AbstractSeam as Seam)
from typing import (Optional, Any)

class ServiceHealth(AbstractServiceHealth):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
