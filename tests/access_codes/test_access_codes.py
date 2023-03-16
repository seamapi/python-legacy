from seamapi import Seam
from seamapi.types import SeamAPIException
from tests.fixtures.run_august_factory import run_august_factory
from tests.fixtures.run_salto_factory import run_salto_factory
import pytest


def test_access_codes(seam: Seam):
    run_august_factory(seam)

    all_devices = seam.devices.list()
    some_device = all_devices[0]

    created_access_code = seam.access_codes.create(
        some_device.device_id, "Test code", "4444"
    )
    assert created_access_code.name == "Test code"
    assert created_access_code.status == "setting"

    access_codes = seam.access_codes.list(some_device.device_id)
    assert len(access_codes) == 1

    access_code = seam.access_codes.get(created_access_code.access_code_id)
    assert access_code.code == "4444"

    with pytest.raises(SeamAPIException):
        seam.access_codes.create(some_device.device_id, "Duplicate Access Code", "4444")

    access_code = seam.access_codes.update(access_code, name="Updated name")
    assert access_code.name == "Updated name"

    delete_action_attempt = seam.access_codes.delete(created_access_code)
    assert delete_action_attempt.status == "success"

    access_codes = seam.access_codes.create_multiple(devices=all_devices)
    assert len(access_codes) == len(all_devices)
    assert len(all_devices) > 1
    assert len(set([ac.common_code_key for ac in access_codes])) == 1


def test_access_codes_create_wait_for_code(seam: Seam):
    run_august_factory(seam)

    all_devices = seam.devices.list()
    some_device = all_devices[0]

    created_access_code = seam.access_codes.create(
        some_device.device_id, "Test code", "4445", wait_for_code=True
    )

    assert created_access_code.name == "Test code"
    assert created_access_code.code == "4445"

    with pytest.raises(RuntimeError) as excinfo:
        seam.access_codes.create(
            some_device.device_id,
            "Test code",
            "4445",
            wait_for_code=True,
            starts_at="3001-01-01",
            ends_at="3001-01-03",
        )
    assert "future time bound code" in str(excinfo.value)
