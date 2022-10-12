import responses
from seamapi import Seam


@responses.activate
def test_sends_error_to_sentry(seam: Seam, monkeypatch):
    rsp = responses.Response(
      method="GET",
      url=seam.api_url + "/devices/list",
      # Missing top-level `devices` key
      json={"foo": []},
      headers={"seam-request-id": "1234"},
    )
    responses.add(rsp)

    sentry_init_args = {}
    sentry_dsn = "https://sentry.io/123"
    monkeypatch.setenv("SENTRY_DSN", sentry_dsn)
    monkeypatch.setattr("sentry_sdk.init", lambda *a, **kw: sentry_init_args.update(kw))

    client_with_sentry = Seam(
      api_key=seam.api_key,
      api_url=seam.api_url,
      should_report_exceptions=True,
    )

    assert sentry_init_args["dsn"] == sentry_dsn
    assert sentry_init_args["default_integrations"] is False

    sentry_capture_exception_calls = []
    monkeypatch.setattr("sentry_sdk.capture_exception", lambda *a, **kw: sentry_capture_exception_calls.append((a, kw)))

    sentry_add_breadcrumb_calls = []
    monkeypatch.setattr("sentry_sdk.add_breadcrumb", lambda *a, **kw: sentry_add_breadcrumb_calls.append((a, kw)))
    try:
      client_with_sentry.devices.list()
      assert False
    except:
      pass

    assert rsp.call_count == 1

    assert len(sentry_capture_exception_calls) == 1
    assert type(sentry_capture_exception_calls[0][0][0]) is KeyError

    assert len(sentry_add_breadcrumb_calls) == 1
    assert sentry_add_breadcrumb_calls[0][1]['category'] == "http"
    assert sentry_add_breadcrumb_calls[0][1]["data"]["request_id"] == "1234"

@responses.activate
def test_skips_sentry_reporting(seam: Seam, monkeypatch):
    rsp = responses.Response(
      method="GET",
      url=seam.api_url + "/devices/list",
      # Missing top-level `devices` key
      json={"foo": []}
    )
    responses.add(rsp)

    monkeypatch.setenv("SENTRY_DSN", "https://sentry.io/123")
    monkeypatch.setattr("sentry_sdk.init", lambda *a, **kw: None)

    client_without_sentry = Seam(
      api_key=seam.api_key,
      api_url=seam.api_url,
    )

    sentry_capture_exception_calls = []
    monkeypatch.setattr("sentry_sdk.capture_exception", lambda *a, **kw: sentry_capture_exception_calls.append((a, kw)))

    try:
      client_without_sentry.devices.list()
      assert False
    except:
      pass

    assert rsp.call_count == 1

    assert len(sentry_capture_exception_calls) == 0

def test_skips_report_for_known_error(seam: Seam, monkeypatch):
    sentry_init_args = {}
    sentry_dsn = "https://sentry.io/123"
    monkeypatch.setenv("SENTRY_DSN", sentry_dsn)
    monkeypatch.setattr("sentry_sdk.init", lambda *a, **kw: sentry_init_args.update(kw))

    client_without_sentry = Seam(
      api_key=seam.api_key,
      api_url=seam.api_url,
      should_report_exceptions=True
    )

    assert sentry_init_args["dsn"] == sentry_dsn

    sentry_capture_exception_calls = []
    monkeypatch.setattr("sentry_sdk.capture_exception", lambda *a, **kw: sentry_capture_exception_calls.append((a, kw)))

    try:
      client_without_sentry.devices.get("123")
      assert False
    except:
      pass

    assert len(sentry_capture_exception_calls) == 0
