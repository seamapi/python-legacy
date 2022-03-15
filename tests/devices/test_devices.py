from seamapi import Seam
from tests.fixtures.login_via_schlage import login_via_schlage
from seamapi.utils.deep_attr_dict import DeepAttrDict


def test_devices(seam: Seam):
    login_via_schlage(seam)

    devices = seam.devices.list()
    assert len(devices) > 0

    some_device = seam.devices.get(name="FRONT DOOR")
    assert some_device.properties.name == "FRONT DOOR"
