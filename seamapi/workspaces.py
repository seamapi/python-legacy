from seamapi.types import AbstractSeam as Seam


class Workspaces:
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam
