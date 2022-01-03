from seamapi.types import AbstractConnectWebviews, ConnectWebview, AbstractSeam as Seam
import requests
from typing import List


class ConnectWebviews(AbstractConnectWebviews):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self) -> List[ConnectWebview]:
        raise NotImplementedError

    def get(self, connect_webview_id: str) -> ConnectWebview:
        raise NotImplementedError

    def create(self) -> ConnectWebview:
        # requests.post(f"{}")
        raise NotImplementedError
