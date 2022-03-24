from typing import Union

from seamapi.types import (
    AccessCode,
    AccessCodeId,
    ActionAttempt,
    ActionAttemptId,
    ConnectWebview,
    ConnectWebviewId,
    ConnectedAccount,
    ConnectedAccountId,
    Device,
    DeviceId,
    Workspace,
    WorkspaceId,
)


def to_access_code_id(access_code: Union[AccessCodeId, AccessCode]) -> str:
    if isinstance(access_code, str):
        return access_code
    return access_code.access_code_id


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


def to_action_attempt_id(
    action_attempt: Union[ActionAttemptId, ActionAttempt]
) -> str:
    if isinstance(action_attempt, str):
        return action_attempt
    return action_attempt.action_attempt_id


def to_connect_webview_id(
    connect_webview: Union[ConnectWebviewId, ConnectWebview]
) -> str:
    if isinstance(connect_webview, str):
        return connect_webview
    return connect_webview.connect_webview_id


def to_connected_account_id(
    connected_account: Union[ConnectedAccountId, ConnectedAccount]
) -> str:
    if isinstance(connected_account, str):
        return connected_account
    return connected_account.connected_account_id


def to_workspace_id(workspace: Union[WorkspaceId, Workspace]) -> str:
    if isinstance(workspace, str):
        return workspace
    return workspace.workspace_id
