from seamapi.types import (
    AbstractSeam as Seam,
    AbstractWorkspaces,
    Workspace,
    WorkspaceId,
    ResetSandBoxResponse,
)
from typing import Optional, List, Union

from seamapi.utils.convert_to_id import to_workspace_id
from seamapi.utils.report_error import report_error


class Workspaces(AbstractWorkspaces):
    """
    A class used to retrieve workspace data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(workspace=None)
        Gets a list of workspaces
    get(workspace=None)
        Gets a workspace
    reset_sandbox()
        Resets workspace sandbox
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
    def list(
        self,
        workspace: Optional[Union[WorkspaceId, Workspace]] = None,
    ) -> List[Workspace]:
        """Gets a list of workspaces.

        Parameters
        ----------
        workspace : WorkspaceId or Workspace, optional
            Workspace id or Workspace to get latest version of

        Raises
        ------
        Exception
            If workspaces weren't found.
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Workspace
        """

        workspace_id = None if workspace is None else to_workspace_id(workspace)
        res = self.seam.make_request(
            "GET",
            "/workspaces/list",
            params={"workspace_id": workspace_id},
        )
        return [Workspace.from_dict(w) for w in res['workspaces']]

    @report_error
    def get(
        self
    ) -> Workspace:
        """Gets a workspace.

        Parameters
        ----------
        workspace : WorkspaceId or Workspace, optional
            Workspace id or Workspace to get latest version of

        Raises
        ------
        Exception
            If the workspace wasn't found.
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Workspace
        """
        res = self.seam.make_request(
            "GET",
            "/workspaces/get",
        )
        return Workspace.from_dict(res["workspace"])

    @report_error
    def reset_sandbox(self) -> None:
        """Resets workspace sandbox.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ResetSandBoxResponse
        """
        self.seam.make_request(
            "POST",
            "/workspaces/reset_sandbox",
        )

        return ResetSandBoxResponse(
            message="Successfully reset workspace sandbox",
            ok=True,
        )

    @report_error
    def create(
        self,
        name: str,
        connect_partner_name: str,
        is_sandbox: Optional[bool] = None,
        webview_primary_button_color: Optional[str] = None,
        webview_logo_shape: Optional[str] = None,
    ) -> Workspace:
        """Creates a workspace.

        Parameters
        ----------
        name : string
            Workspace name
        connect_partner_name : string
            Name shown on the connect webview
        is_sandbox : string, optional
            If true, creates a sandbox workspace; if false, creates a production workspace. Defaults to false.
        webview_primary_button_color : string, optional
            The color of the primary button in the webview, represented in hex format (e.g., "#RRGGBB").
        webview_logo_shape : string, optional
            The shape of the logo in the webview: "circle" or "square".


        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Workspace
        """

        create_payload = {
            "workspace_name": name,
            "name": name,
            "connect_partner_name": connect_partner_name
        }

        if is_sandbox is not None:
            create_payload["is_sandbox"] = is_sandbox
        if webview_primary_button_color is not None:
            create_payload["webview_primary_button_color"] = webview_primary_button_color
        if webview_logo_shape is not None:
            create_payload["webview_logo_shape"] = webview_logo_shape

        res = self.seam.make_request(
            "POST",
            "/workspaces/create",
            json=create_payload,
        )
        return Workspace.from_dict(res["workspace"])
