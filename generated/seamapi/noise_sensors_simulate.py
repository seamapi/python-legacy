from seamapi.types import (AbstractSimulateNoiseSensors,AbstractSeam as Seam)
from typing import (Optional, Any)

class SimulateNoiseSensors(AbstractSimulateNoiseSensors):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
