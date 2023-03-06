import time
from seamapi import Seam
from tests.fixtures.run_august_factory import run_august_factory

SINCE = "2021-01-01T00:00:00.000Z"
EVENT_TYPE = "device.connected"
FAKE_UUID = "00000000-0000-0000-0000-000000000000"


def test_events(seam: Seam):
    run_august_factory(seam)

    events = seam.events.list(since=SINCE)
    event = next(e for e in events if e["event_type"] == EVENT_TYPE)

    event_by_id = seam.events.get(event_id=event["event_id"])
    assert event_by_id["event_id"] == event["event_id"]

    event_by_type = seam.events.get(event_type=event["event_type"])
    assert event_by_type["event_type"] == event["event_type"]

    event_by_device_id = seam.events.get(device_id=event["device_id"])
    assert event_by_device_id["device_id"] == event["device_id"]

    none_event = seam.events.get(event_id=FAKE_UUID)
    assert none_event is None
