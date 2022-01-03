from seamapi import Seam


def test_init_seam():
    seam = Seam()
    assert seam.api_key
    assert seam.api_url
