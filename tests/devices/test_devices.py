from seamapi import Seam
from seamapi.types import SeamAPIException
from tests.fixtures.run_august_factory import run_august_factory
from seamapi.utils.deep_attr_dict import DeepAttrDict


def test_devices(seam: Seam):
    run_august_factory(seam)

    devices = seam.devices.list()
    assert len(devices) > 0

    connected_account = seam.connected_accounts.list()[0]
    devices = seam.devices.list(connected_account=connected_account)
    assert len(devices) > 0
    devices = seam.devices.list(connected_accounts=[connected_account])
    assert len(devices) > 0

    devices = seam.devices.list(device_type="august_lock")
    assert len(devices) > 0
    devices = seam.devices.list(device_types=["august_lock"])
    assert len(devices) > 0

    devices = seam.devices.list(manufacturer="august")
    assert len(devices) > 0

    device_ids = [devices[0]]
    devices = seam.devices.list(device_ids=device_ids)
    assert len(devices) == 1

    some_device = seam.devices.get(name="Generated Lock 0")
    assert some_device.properties.name == "Generated Lock 0"

    locks = seam.locks.list()
    assert len(locks) > 0

    some_lock = seam.locks.get(device=(some_device))
    assert some_lock.device_id == some_device.device_id

    assert some_lock.properties.locked == True

    seam.locks.unlock_door(device=(some_device.device_id))
    some_unlocked_lock = seam.locks.get(device=(some_device))
    assert some_unlocked_lock.properties.locked == False

    seam.locks.lock_door(device=(some_device))
    some_locked_lock = seam.locks.get(device=(some_device))
    assert some_locked_lock.properties.locked == True

    seam.devices.update(device=(some_device), name="Updated lock")
    some_updated_lock = seam.locks.get(device=(some_device))
    assert some_updated_lock.properties.name == "Updated lock"

    devices = seam.devices.list()
    seam.devices.delete(device=(some_updated_lock))
    assert len(seam.devices.list()) == len(devices) - 1

    # Test custom exception
    try:
        seam.devices.get(name="foo")
        assert False
    except SeamAPIException as error:
        assert error.status_code == 404
        assert type(error.request_id) == str
        assert error.metadata["type"] == "device_not_found"

    stable_device_providers = seam.devices.list_device_providers(
        provider_category="stable"
    )
    assert len(stable_device_providers) > 0


def test_unmanaged_devices(seam: Seam):
    run_august_factory(seam)

    devices = seam.devices.list()
    assert len(devices) > 0

    unmanaged_devices = seam.devices.unmanaged.list()
    assert len(unmanaged_devices) == 0

    device = devices[0]

    seam.devices.update(device=device, is_managed=False)
    unmanaged_devices = seam.devices.unmanaged.list()
    assert len(unmanaged_devices) == 1

    connected_account = seam.connected_accounts.list()[0]
    devices = seam.devices.unmanaged.list(connected_account=connected_account)
    assert len(devices) > 0
    devices = seam.devices.unmanaged.list(
        connected_accounts=[connected_account]
    )
    assert len(devices) > 0

    devices = seam.devices.unmanaged.list(device_type="august_lock")
    assert len(devices) > 0
    devices = seam.devices.unmanaged.list(device_types=["august_lock"])
    assert len(devices) > 0

    devices = seam.devices.unmanaged.list(manufacturer="august")
    assert len(devices) > 0

    seam.devices.unmanaged.update(device=device, is_managed=True)
    unmanaged_devices = seam.devices.unmanaged.list()
    assert len(unmanaged_devices) == 0
