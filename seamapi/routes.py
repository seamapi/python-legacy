from .types import AbstractRoutes
from .workspaces import Workspaces
from .devices import Devices
from .events import Events
from .connected_accounts import ConnectedAccounts
from .connect_webviews import ConnectWebviews
from .locks import Locks
from .access_codes import AccessCodes
from .action_attempts import ActionAttempts

class Routes(AbstractRoutes):
    def __init__(self):
      self.workspaces = Workspaces(seam=self)
      self.connected_accounts = ConnectedAccounts(seam=self)
      self.connect_webviews = ConnectWebviews(seam=self)
      self.devices = Devices(seam=self)
      self.events = Events(seam=self)
      self.locks = Locks(seam=self)
      self.access_codes = AccessCodes(seam=self)
      self.action_attempts = ActionAttempts(seam=self)

    def make_request(self):
      raise NotImplementedError()
