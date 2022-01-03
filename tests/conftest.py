import pytest
from seamapi import Seam
import requests
from dotenv import load_dotenv
from typing import Any


@pytest.fixture(autouse=True)
def dotenv_fixture():
    load_dotenv()


@pytest.fixture
def seam(dotenv_fixture: Any):
    seam = Seam()
    requests.post(
        f"{seam.api_url}/workspaces/reset_sandbox",
        headers={"Authorization": f"Bearer {seam.api_key}"},
    )
    yield seam
