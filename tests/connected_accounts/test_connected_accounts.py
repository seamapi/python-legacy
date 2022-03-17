from seamapi import Seam
from tests.fixtures.login_via_schlage import login_via_schlage


def test_connected_accounts(seam: Seam):
    login_via_schlage(seam)

    connected_accounts = seam.connected_accounts.list()
    assert len(connected_accounts) > 0

    connected_account_id = connected_accounts[0].connected_account_id
    connected_account = seam.connected_accounts.get(connected_account_id)
    assert connected_account.connected_account_id == connected_account_id
