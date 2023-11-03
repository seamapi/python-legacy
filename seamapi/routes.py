from .types import AbstractRoutes
from .access_codes import AccessCodes
from .action_attempts import ActionAttempts
from .client_sessions import ClientSessions
from .connect_webviews import ConnectWebviews
from .connected_accounts import ConnectedAccounts
from .devices import Devices
from .events import Events
from .health import Health
from .locks import Locks
from .thermostats import Thermostats
from .user_identities import UserIdentities
from .webhooks import Webhooks
from .workspaces import Workspaces

class Routes(AbstractRoutes):
  def __init__(self):
    self.access_codes = AccessCodes(seam=self)
    self.action_attempts = ActionAttempts(seam=self)
    self.client_sessions = ClientSessions(seam=self)
    self.connect_webviews = ConnectWebviews(seam=self)
    self.connected_accounts = ConnectedAccounts(seam=self)
    self.devices = Devices(seam=self)
    self.events = Events(seam=self)
    self.health = Health(seam=self)
    self.locks = Locks(seam=self)
    self.thermostats = Thermostats(seam=self)
    self.user_identities = UserIdentities(seam=self)
    self.webhooks = Webhooks(seam=self)
    self.workspaces = Workspaces(seam=self)

  def make_request(self):
    raise NotImplementedError()