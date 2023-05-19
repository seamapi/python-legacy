from seamapi import Seam
from tests.fixtures.run_august_factory import run_august_factory

EMAIL = "user-4@example.com"


def test_connected_accounts(seam: Seam):
    run_august_factory(seam)

    connected_accounts = seam.connected_accounts.list()
    assert len(connected_accounts) > 0

    connected_account_id = connected_accounts[0].connected_account_id
    connected_account = seam.connected_accounts.get(connected_account_id)
    email_account = seam.connected_accounts.get(email=EMAIL)

    assert connected_account.connected_account_id == connected_account_id
    assert email_account.connected_account_id == connected_account_id

    seam.connected_accounts.delete(connected_account)
    assert len(seam.connected_accounts.list()) == 0

    # Assert that an Exception is raised for the .get() method when
    # connected_account and email parameters are not provided.
    try:
        seam.connected_accounts.get()
    except Exception as e:
        assert (
            str(e)
            == "Must provide either ConnectedAccount (ConnectedAccount or ConnectedAccountId) or Email"
        )
