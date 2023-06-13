from seamapi.types import AbstractNoiseSensors, AbstractSeam as Seam
from seamapi.noise_thresholds import NoiseThresholds
from seamapi.utils.report_error import report_error


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
        An instance of the NoiseThresholds class designed to interact with noise thresholds
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
        self._noise_thresholds = NoiseThresholds(seam=seam)

    @property
    def noise_thresholds(self) -> NoiseThresholds:
        return self._noise_thresholds

    @report_error
    def list_noise_levels(self, noise_threshold_id):
        raise NotImplementedError()
