from seamapi.types import AbstractConnectWebviews, ConnectWebview
from typing import List


class ConnectWebviews(AbstractConnectWebviews):
    def list(self) -> List[ConnectWebview]:
        raise NotImplementedError

    def get(self, connect_webview_id: str) -> ConnectWebview:
        raise NotImplementedError

    def create(self) -> ConnectWebview:
        raise NotImplementedError
