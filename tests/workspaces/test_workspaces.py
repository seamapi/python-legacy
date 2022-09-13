from seamapi import Seam
from tests.fixtures.run_august_factory import run_august_factory


def test_workspaces(seam: Seam):
    run_august_factory(seam)

    ws = seam.workspaces.get()
    assert ws.is_sandbox == True

    reset_sandbox_result = seam.workspaces.reset_sandbox()
    assert reset_sandbox_result is not None

    ws_list = seam.workspaces.list()
    assert len(ws_list) > 0
