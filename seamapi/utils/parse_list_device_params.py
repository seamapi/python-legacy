from seamapi.types import (
    ConnectWebview,
    ConnectWebviewId,
    ConnectedAccount,
    ConnectedAccountId,
    Device,
    DeviceId,
    DeviceType,
)
from typing import List, Union, Optional
from seamapi.utils.convert_to_id import (
    to_connect_webview_id,
    to_connected_account_id,
    to_device_id,
)


def parse_list_device_params(
    connected_account: Union[ConnectedAccountId, ConnectedAccount] = None,
    connected_accounts: List[
        Union[ConnectedAccountId, ConnectedAccount]
    ] = None,
    connect_webview: Union[ConnectWebviewId, ConnectWebview] = None,
    device_type: Optional[DeviceType] = None,
    device_types: Optional[List[DeviceType]] = None,
    device_ids: Optional[List[Union[DeviceId, Device]]] = None,
    manufacturer: Optional[str] = None,
    limit: Optional[float] = None,
    created_before: Optional[str] = None,
) -> dict:
    params = {}
    if connected_account:
        params["connected_account_id"] = to_connected_account_id(
            connected_account
        )
    if connected_accounts:
        params["connected_account_ids"] = [
            to_connected_account_id(ca) for ca in connected_accounts
        ]
    if connect_webview:
        params["connect_webview_id"] = to_connect_webview_id(connect_webview)
    if device_type:
        params["device_type"] = device_type
    if device_types is not None:
        params["device_types"] = device_types
    if device_ids is not None:
        params["device_ids"] = [to_device_id(d) for d in device_ids]
    if manufacturer:
        params["manufacturer"] = manufacturer
    if limit:
        params["limit"] = limit
    if created_before:
        params["created_before"] = created_before

    return params
