from seamapi import Seam
from tests.fixtures.run_august_factory import run_august_factory


def test_connected_accounts(seam: Seam):
    run_august_factory(seam)

    connected_accounts = seam.connected_accounts.list()
    assert len(connected_accounts) > 0

    connected_account_id = connected_accounts[0].connected_account_id
    connected_account = seam.connected_accounts.get(connected_account_id)
    assert connected_account.connected_account_id == connected_account_id
