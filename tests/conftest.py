import pytest
from seamapi import Seam
import time
import requests
from dotenv import load_dotenv
from typing import Any
from dataclasses import dataclass
import sys
from testcontainers.postgres import PostgresContainer
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


@pytest.fixture(autouse=True)
def dotenv_fixture():
    load_dotenv()


@dataclass
class SeamBackend:
    url: str
    sandbox_api_key: str


# TODO this should use scope="session", but there's some issue, this would
# dramatically reduce test time to switch
@pytest.fixture(scope="function")
def seam_backend():
    with PostgresContainer("postgres:13", dbname="postgres") as pg:
        db_host = "host.docker.internal" if sys.platform == "darwin" else "172.17.0.1"
        db_url = f"postgresql://test:test@{db_host}:{pg.get_exposed_port(pg.port_to_expose)}/postgres"
        with DockerContainer("ghcr.io/seamapi/seam-connect").with_env(
            "DATABASE_URL",
            db_url,
        ).with_env("POSTGRES_DATABASE", "postgres").with_env(
            "NODE_ENV", "test"
        ).with_env(
            "POSTGRES_HOST", db_host
        ).with_env(
            "SERVER_BASE_URL", "http://localhost:3020"
        ).with_env(
            "SEAMTEAM_ADMIN_PASSWORD", "1234"
        ).with_env(
            "PORT", "3020"
        ).with_bind_ports(
            3020, 3020
        ).with_command(
            "start:for-integration-testing"
        ) as sc_container:
            wait_for_logs(sc_container, r"started server", timeout=20)
            requests.get("http://localhost:3020/health")
            yield SeamBackend(
                url="http://localhost:3020",
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
