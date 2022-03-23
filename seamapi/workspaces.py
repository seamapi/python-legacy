from seamapi.types import AbstractSeam as Seam, AbstractWorkspaces, Workspace
from typing import Optional, List
import requests


class Workspaces(AbstractWorkspaces):
    """
    A class used to retreive workspace data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : dict
        Initial seam class

    Methods
    -------
    list(workspace_id=None)
        Gets a list of workspaces
    get(workspace_id=None)
        Gets a workspace
    reset_sandbox()
        Resets workspace sandbox
    """
  
    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : dict
          Intial seam class
        """

        self.seam = seam

    def list(self, workspace_id: Optional[str] = None) -> List[Workspace]:
        """Gets a list of workspaces.

        Parameters
        ----------
        workspace_id : str, optional
            Workspace id

        Raises
        ------
        Exception
            If workspaces weren't found.
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of workspaces.
        """

        res = requests.get(
            f"{self.seam.api_url}/workspaces/list",
            params={"workspace_id": workspace_id},
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if res.status_code == 404:
            raise Exception("workspaces not found")  # TODO custom exception
        if res.status_code != 200:
            raise Exception(res.text)
        res_json = res.json()
        return res_json['workspaces']

    def get(self, workspace_id: Optional[str] = None) -> Workspace:
        """Gets a workspace.

        Parameters
        ----------
        workspace_id : str, optional
            Workspace id

        Raises
        ------
        Exception
            If the workspace wasn't found.
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A workspace dict.
        """

        res = requests.get(
            f"{self.seam.api_url}/workspaces/get",
            params={"workspace_id": workspace_id},
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if res.status_code == 404:
            raise Exception("workspace not found")  # TODO custom exception
        if res.status_code != 200:
            raise Exception(res.text)
        res_json = res.json()
        return Workspace(
            workspace_id=res_json["workspace"]["workspace_id"],
            name=res_json["workspace"]["name"],
            is_sandbox=res_json["workspace"]["is_sandbox"],
        )

    def reset_sandbox(self) -> None:
        """Resets workspace sandbox.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            None
        """

        res = requests.post(
            f"{self.seam.api_url}/workspaces/reset_sandbox",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        return None
