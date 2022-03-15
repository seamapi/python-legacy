from seamapi import Seam
from tests.fixtures.login_via_schlage import login_via_schlage


def test_devices(seam: Seam):
    login_via_schlage(seam)

    devices = seam.devices.list()

    some_device = seam.devices.get(name="FRONT DOOR")
    print(some_device)

    print(devices)

    pass
