from seamapi.types import AbstractNoiseSensors, AbstractSeam as Seam
from seamapi.noise_thresholds import NoiseThresholds


class NoiseSensors(AbstractNoiseSensors):
    """
    A class to interact with noise sensors through the Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Properties
    -------
    noise_thresholds
        An instance of the NoiseThresholds class to interact with noise thresholds
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Intial seam class
        """
        self.seam = seam
        self.noise_thresholds = NoiseThresholds(seam=seam)
