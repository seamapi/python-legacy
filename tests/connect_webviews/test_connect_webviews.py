from seamapi import Seam


def test_connect_webviews(seam: Seam):
    created_webview = seam.connect_webviews.create(accepted_providers=["schlage"])
    assert created_webview.url is not None

    webview = seam.connect_webviews.get(created_webview.connect_webview_id)
    assert webview.connect_webview_id == created_webview.connect_webview_id

    webviews = seam.connect_webviews.list()
    assert len(webviews) > 0

    seam.connect_webviews.delete(created_webview)
    webviews = seam.connect_webviews.list()
    assert len(webviews) == 0