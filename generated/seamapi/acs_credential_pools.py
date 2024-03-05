from seamapi.types import (AbstractCredentialPoolsAcs,AbstractSeam as Seam)
from typing import (Optional, Any)

class CredentialPoolsAcs(AbstractCredentialPoolsAcs):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
