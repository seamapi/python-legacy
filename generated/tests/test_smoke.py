from seamapi import Seam


def test_get_devices(seam: Seam):
    devices_response = seam.devices.list()
    assert devices_response[0].device_id


def test_create_access_code(seam: Seam):
    access_code = seam.access_codes.create(device_id="august_device_1", code="1234")
    assert access_code.status == "setting"
    assert access_code.code == "1234"