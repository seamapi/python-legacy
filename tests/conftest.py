import pytest
from seamapi import Seam
import time
import requests
from dotenv import load_dotenv
from typing import Any
from dataclasses import dataclass
from testcontainers.postgres import PostgresContainer
from testcontainers.core.container import DockerContainer


@pytest.fixture(autouse=True)
def dotenv_fixture():
    load_dotenv()


@dataclass
class SeamBackend:
    url: str
    sandbox_api_key: str


@pytest.fixture
def seam_backend():
    with PostgresContainer("postgres:13", port=5499) as pg:
        with DockerContainer("seam-connect").with_env(
            "DATABASE_URL", pg.get_connection_url()
        ).with_env("NODE_ENV", "test").with_env(
            "SERVER_BASE_URL", "http://localhost:3021"
        ).with_env(
            "SEAMTEAM_ADMIN_PASSWORD", "1234"
        ).with_bind_ports(
            3020, 3021
        ).with_command(
            "start:for-integration-testing"
        ) as sc_container:
            # print(pg.get_connection_url())
            time.sleep(200)  # TODO wait for log message "ready - started server"
            requests.get("http://localhost:3021/health")
            yield SeamBackend(
                url="http://localhost:3021",
                sandbox_api_key="seam_sandykey_0000000000000000000sand",
            )


@pytest.fixture
def seam(seam_backend: Any, dotenv_fixture: Any):
    seam = Seam(api_url=seam_backend.url, api_key=seam_backend.sandbox_api_key)
    requests.post(
        f"{seam.api_url}/workspaces/reset_sandbox",
        headers={"Authorization": f"Bearer {seam.api_key}"},
    )
    yield seam
