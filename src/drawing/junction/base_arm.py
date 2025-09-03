from pydantic import Field
from ..base_config import BaseConfig
import gdsfactory as gf

class BaseArmConfig(BaseConfig):
    """
    Base configuration for arm components.
    Attributes:
        layer (LayerSpec): Layer specification for the arm component.
    """

    CONNECTION_PORT_NAME: str = Field("connection", exclude=True)
    GAP_PORT_NAME: str = Field("gap", exclude=True)
    
    def __eq__(self, other):
        if not isinstance(other, BaseArmConfig):
            return NotImplemented
        # include layer if it affects build
        return self.layer == other.layer

    def __hash__(self):
        # same fields as __eq__
        return hash((self.layer))

    def build(self) -> gf.Component:
        raise NotImplementedError("Subclasses should implement this method.")

    def total_length(self) -> float:
        """
        Returns the total length of the arm.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def validate(self) -> None:
        pass