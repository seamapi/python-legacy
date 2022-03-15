from seamapi import Seam


# def test_init_seam():
#     seam = Seam()
#     assert seam.api_key
#     assert seam.api_url


def test_init_seam_with_fixture(seam: Seam):
    assert seam.api_key
    assert seam.api_url
    assert "https" in seam.api_url and "localhost" in seam.api_url
