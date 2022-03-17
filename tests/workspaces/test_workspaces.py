from seamapi import Seam
from tests.fixtures.login_via_schlage import login_via_schlage


def test_workspaces(seam: Seam):
    login_via_schlage(seam)

    ws = seam.workspaces.get()
    assert ws.is_sandbox == True

    reset_sandbox_result = seam.workspaces.reset_sandbox()
    assert reset_sandbox_result is None

    # seam.workspaces.list() - not implemented
