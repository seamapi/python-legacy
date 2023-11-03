from seamapi.types import (AbstractHealth,AbstractSeam as Seam)
from typing import (Optional, Any)

class Health(AbstractHealth):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
