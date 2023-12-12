from seamapi import Seam


def test_workspaces(seam: Seam):
    webhook = seam.webhooks.create(
        url="https://example.com", event_types=["connected_account.connected"]
    )
    assert webhook.url == "https://example.com"

    webhook = seam.webhooks.get(webhook)
    assert webhook is not None

    webhook_list = seam.webhooks.list()
    assert len(webhook_list) > 0

    seam.webhooks.delete(webhook)
    webhook_list = seam.webhooks.list()
    assert len(webhook_list) == 0
