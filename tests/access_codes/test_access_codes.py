from seamapi import Seam
from seamapi.types import SeamApiException
import pytest


def test_access_codes(seam: Seam):

    all_devices = seam.devices.list()
    some_device = all_devices[0]

    created_access_code = seam.access_codes.create(
        device_id=some_device.device_id, name="Test code", code="4444" 
    )
    assert created_access_code.name == "Test code"
    assert created_access_code.status == "setting"

    seam.access_codes.create(device_id=some_device.device_id, name="Test code 2", code="5555")

    access_codes = seam.access_codes.list(device_id=some_device.device_id)
    assert len(access_codes) == 2
    access_codes = seam.access_codes.list(
        device_id=some_device.device_id, access_code_ids=[created_access_code.access_code_id]
    )
    assert len(access_codes) == 1

    access_code = seam.access_codes.get(access_code_id=created_access_code.access_code_id)
    assert access_code.code == "4444"

    # with pytest.raises(SeamApiException):
    #     seam.access_codes.create(
    #         device_id=some_device.device_id, name="Duplicate Access Code", code="4444"
    #     )

    access_code = seam.access_codes.update(access_code_id=access_code.access_code_id, name="Updated name")
    assert access_code.name == "Updated name"

    access_code = seam.access_codes.update(
        access_code_id=access_code.access_code_id,
        type="time_bound",
        starts_at="3001-01-01",
        ends_at="3001-01-03",
    )
    assert access_code.type == "time_bound"

    delete_action_attempt = seam.access_codes.delete(access_code_id=created_access_code.access_code_id)
    assert delete_action_attempt.status == "success"

    access_codes = seam.access_codes.create_multiple(device_ids=[device.device_id for device in all_devices])
    assert len(set([ac.common_code_key for ac in access_codes])) == 1


def test_access_codes_create_wait_for_code(seam: Seam):

    all_devices = seam.devices.list()
    some_device = all_devices[0]

    created_access_code = seam.access_codes.create(
        device_id=some_device.device_id, name="Test code", code="4445", wait_for_code=True 
    )

    assert created_access_code.name == "Test code"
    assert created_access_code.code == "4445"

    with pytest.raises(RuntimeError) as excinfo:
        seam.access_codes.create(
            device_id=some_device.device_id,
            name="Test code",
            code="4445",
            wait_for_code=True,
            starts_at="3001-01-01",
            ends_at="3001-01-03",
        )
    assert "future time bound code" in str(excinfo.value)
