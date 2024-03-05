import pytest
import random
import string
from seamapi import Seam


@pytest.fixture(scope="function")
def seam():
    r = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    seam = Seam(api_url=f"https://{r}.fakeseamconnect.seam.vc", api_key="seam_apikey1_token")
    yield seam