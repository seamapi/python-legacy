import random
import string
import pytest
from seamapi import Seam
from dotenv import load_dotenv
from typing import Any
from dataclasses import dataclass


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
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    yield SeamBackend(
        url=f"https://{random_string}.fakeseamconnect.seam.vc",
        sandbox_api_key="seam_apikey1_token",
    )


@pytest.fixture
def seam(seam_backend: Any):
    seam = Seam(api_url=seam_backend.url, api_key=seam_backend.sandbox_api_key)
    # seam.make_request("POST", "/workspaces/reset_sandbox")
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
