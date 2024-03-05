from seamapi.types import (AbstractCredentialsAcs,AbstractSeam as Seam)
from typing import (Optional, Any)

class CredentialsAcs(AbstractCredentialsAcs):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
