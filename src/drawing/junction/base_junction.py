from drawing.junction.base_arm import BaseArmConfig
from pydantic import ConfigDict, Field
from ..base_config import BaseConfig
import gdsfactory as gf
from typing import Literal

junctionTypeEnum = Literal["DOLAN", "DOLATHAN", "MANHANTAN"]

class BaseJunctionConfig(BaseConfig):
    """
    Base configuration for junction components.
    Attributes:
        gap_length (float): Length of the gap.
        layer (LayerSpec): Layer specification for the junction component.
        gap_layer (LayerSpec): Layer specification for the gap.
        gap_create (bool): Whether to create a gap in the junction.
    """
    
    gap_length: float = 1.0
    gap_layer: gf.typings.LayerSpec = (1,11)
    gap_create: bool = True

    junction_type: junctionTypeEnum = "DOLAN"

    LEFT_PREFIX: str = Field("left_", exclude=True)
    RIGHT_PREFIX: str = Field("right_", exclude=True)

    model_config = ConfigDict(frozen=True)
    
    def total_length(self) -> float:
        """
        Returns the total length of the junction.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_left_arm_config(self) -> BaseArmConfig:
        raise NotImplementedError("Subclasses should implement this method.")

    def get_right_arm_config(self) -> BaseArmConfig:
        raise NotImplementedError("Subclasses should implement this method.")

    def validate(self) -> None:
        if self.left_arm is None: 
            raise ValueError("Left arm must be defined.")
        if self.right_arm is None:
            raise ValueError("Right arm must be defined.")