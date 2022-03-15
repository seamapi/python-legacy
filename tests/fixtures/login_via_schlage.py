from seamapi import Seam
import time
import requests


def login_via_schlage(seam: Seam):
    webview = seam.connect_webviews.create(accepted_providers=["schlage"])
    print(seam.workspaces.get())
    print(webview)

    # This is an internal endpoint that will be removed, don't use it, see how
    # it says "internal" there? It's not going to stick around.
    schlage_login_res = requests.post(
        f"{seam.api_url}/internal/schlage/login",
        json={
            "email": "jane@example.com",
            "password": "1234",
            "connect_webview_id": webview.connect_webview_id,
        },
    ).json()

    # We've completed a webview login, which will load devices into this
    # workspace
    pass
