from seamapi.types import (AbstractCredentialProvisioningAutomationsAcs,AbstractSeam as Seam)
from typing import (Optional, Any)

class CredentialProvisioningAutomationsAcs(AbstractCredentialProvisioningAutomationsAcs):
  seam: Seam

  def __init__(self, seam: Seam):
    self.seam = seam
