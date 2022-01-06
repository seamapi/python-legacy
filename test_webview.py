from seamapi import Seam


def test_create_webview():
    seam = Seam()

    seam.connect_webviews.create(accepted_providers=["august"])

    # seam.
