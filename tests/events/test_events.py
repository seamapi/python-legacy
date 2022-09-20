from seamapi import Seam
from tests.fixtures.run_august_factory import run_august_factory

SINCE="2021-01-01T00:00:00.000Z"
EVENT_TYPE = "device.connected"

def test_events(seam: Seam):
    run_august_factory(seam)

    events = seam.events.list(since=SINCE)
    assert events[0]['event_type'] == EVENT_TYPE