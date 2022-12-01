import os
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
        with DockerContainer(
            os.environ.get(
                "SEAM_CONNECT_IMAGE", "ghcr.io/seamapi/seam-connect"
            )
        ).with_env(
            "DATABASE_URL", pg.get_connection_url()
        ).with_env(
            "POSTGRES_DATABASE", "postgres"
        ).with_env(
            "NODE_ENV", "test"
        ).with_env(
            "POSTGRES_HOST", pg.get_container_host_ip()
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
    seam.make_request("POST", "/workspaces/reset_sandbox")
    yield seam

@pytest.fixture
def fake_sentry(monkeypatch):
    sentry_dsn = "https://key@sentry.io/123"

    monkeypatch.setenv("SENTRY_DSN", sentry_dsn)

    sentry_init_args = {}
    sentry_capture_exception_calls = []
    sentry_add_breadcrumb_calls = []
    class TestSentryClient(object):
        def __init__(self, *args, **kwargs):
            sentry_init_args.update(kwargs)
        def set_context(self, *args, **kwargs):
            pass

    monkeypatch.setattr("sentry_sdk.Client", TestSentryClient)

    class TestSentryScope(object):
        def set_context(self, *args, **kwargs):
            pass

    class TestSentryHub(object):
        def __init__(self, *args, **kwargs):
          self.scope = TestSentryScope()
        def capture_exception(self, *args, **kwargs):
          sentry_capture_exception_calls.append((args, kwargs))
        def add_breadcrumb(self, *args, **kwargs):
            sentry_add_breadcrumb_calls.append((args, kwargs))

    monkeypatch.setattr("sentry_sdk.Hub", TestSentryHub)

    yield {
        "sentry_init_args": sentry_init_args,
        "sentry_capture_exception_calls": sentry_capture_exception_calls,
        "sentry_add_breadcrumb_calls": sentry_add_breadcrumb_calls,
        "sentry_dsn": sentry_dsn,
    }
