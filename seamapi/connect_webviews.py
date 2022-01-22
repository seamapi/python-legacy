from seamapi.types import (
    AbstractConnectWebviews,
    ConnectWebview,
    AbstractSeam as Seam,
    AcceptedProvider,
)
import requests
from typing import List, Optional


class ConnectWebviews(AbstractConnectWebviews):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self) -> List[ConnectWebview]:
        res = requests.post(
            f"{self.seam.api_url}/connect_webviews/list",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webviews = res.json()["connect_webviews"]
        return [
            ConnectWebview(
                connect_webview_id=json_webview["connect_webview_id"],
                status=json_webview["status"],
                url=json_webview["url"],
                login_successful=json_webview["login_successful"],
                connected_account_id=json_webview["connected_account_id"],
            )
            for json_webview in json_webviews
        ]

    def get(self, connect_webview_id: str) -> ConnectWebview:
        res = requests.post(
            f"{self.seam.api_url}/connect_webviews/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"connect_webview_id": connect_webview_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webview = res.json()["connect_webview"]
        return ConnectWebview(
            connect_webview_id=json_webview["connect_webview_id"],
            status=json_webview["status"],
            url=json_webview["url"],
            login_successful=json_webview["login_successful"],
            connected_account_id=json_webview["connected_account_id"],
        )

    def create(
        self, accepted_providers: Optional[List[AcceptedProvider]] = []
    ) -> ConnectWebview:
        res = requests.post(
            f"{self.seam.api_url}/connect_webviews/create",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"accepted_providers": accepted_providers},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webview = res.json()["connect_webview"]
        return ConnectWebview(
            connect_webview_id=json_webview["connect_webview_id"],
            status=json_webview["status"],
            url=json_webview["url"],
            login_successful=json_webview["login_successful"],
            connected_account_id=None,
        )
