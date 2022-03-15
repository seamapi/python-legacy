from seamapi import Seam


def test_connect_webviews(seam: Seam):
    webview = seam.connect_webviews.create(accepted_providers=["schlage"])

    assert webview.url is not None
