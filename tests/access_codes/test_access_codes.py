from seamapi import Seam
from tests.fixtures.login_via_schlage import login_via_schlage


def test_access_codes(seam: Seam):
    login_via_schlage(seam)

    some_device = seam.devices.list()[0]

    created_access_code = seam.access_codes.create(some_device.device_id, "Test code", "4444")
    assert created_access_code.name == "Test code"

    access_codes = seam.access_codes.list(some_device.device_id)
    assert len(access_codes) == 1

    access_code = seam.access_codes.get(created_access_code.access_code_id)
    assert access_code.code == "4444"

    delete_action_attempt = seam.access_codes.delete(created_access_code)
    assert delete_action_attempt.status == "success"
