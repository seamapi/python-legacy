from seamapi.types import (
    AbstractSeam as Seam,
    AbstractWebhooks,
    Webhook,
    WebhookId,
)
import time
from typing import List, Union, Optional, cast
import requests
from seamapi.utils.convert_to_id import (
    to_connect_webview_id,
    to_connected_account_id,
    to_device_id,
    to_webhook_id,
)
from seamapi.utils.report_error import report_error


class Webhooks(AbstractWebhooks):
    """
    A class used to interact with webhooks API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    create(url, event_types=None)
        Creates a new webhook
    delete(webhook_id)
        Deletes a webhook
    get(webhook_id)
        Fetches a webhook
    list()
        Lists webhooks
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Initial seam class
        """

        self.seam = seam

    @report_error
    def create(
        self,
        url: str,
        event_types: Optional[list] = None,
    ) -> Webhook:
        """Creates a new webhook.

        Parameters
        ----------
        url : str
            URL to send webhook events to
        event_types : Optional[List[str]]
            List of event types to send to webhook eg. ["connected_account.connected"]. Defaults to ["*"]

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A webhook.
        """
        create_payload = {"url": url}
        if event_types is not None:
            create_payload["event_types"] = event_types

        res = self.seam.make_request(
            "POST",
            "/webhooks/create",
            json=create_payload,
        )

        return Webhook.from_dict(res["webhook"])

    @report_error
    def delete(
        self,
        webhook: Union[WebhookId, Webhook],
    ) -> bool:
        """Deletes a webhook.

        Parameters
        ----------
        webhook : Union[WebhookId, Webhook]
            Webhook ID or Webhook

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Boolean.
        """

        res = self.seam.make_request(
            "DELETE",
            "/webhooks/delete",
            json={"webhook_id": to_webhook_id(webhook)},
        )

        return True

    @report_error
    def get(
        self,
        webhook: Union[WebhookId, Webhook],
    ) -> Webhook:
        """Fetches a webhook.

        Parameters
        ----------
        webhook : Union[WebhookId, Webhook]
            Webhook ID or Webhook

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A webhook.
        """

        res = self.seam.make_request(
            "GET",
            "/webhooks/get",
            params={"webhook_id": to_webhook_id(webhook)},
        )

        return Webhook.from_dict(res["webhook"])

    @report_error
    def list(
        self,
    ) -> List[Webhook]:
        """Lists webhooks.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of webhooks.
        """

        res = self.seam.make_request(
            "GET",
            "/webhooks/list",
        )

        return [Webhook.from_dict(w) for w in res["webhooks"]]
