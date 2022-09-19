from seamapi import Seam
from tests.fixtures.run_august_factory import run_august_factory
from seamapi.utils.deep_attr_dict import DeepAttrDict


def test_devices(seam: Seam):
    run_august_factory(seam)

    devices = seam.devices.list()
    assert len(devices) > 0

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

    seam.devices.delete(device=(some_updated_lock))
    assert len(seam.devices.list()) == len(devices) - 1