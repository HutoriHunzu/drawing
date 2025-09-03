from typing import Self
from gdsfactory.typings import LayerSpec
from ..shared import DEFAULT_LAYER
import gdsfactory as gf
from .base_arm import BaseArmConfig
from pydantic import ConfigDict, computed_field
from pyparsing import cached_property

class RegularArmConfig(BaseArmConfig):
    """
    Configuration for a rectangular arm component.
    Attributes:
        layer (LayerSpec): Layer specification for the regular arm component.
        length (float): Length of the arm.
        width (float): Width of the arm.
    """

    length: float = 10.0
    width: float = 1.0

    def __eq__(self, other):
        if not isinstance(other, RegularArmConfig):
            return NotImplemented
        # include layer if it affects build
        return (self.length, self.width, self.layer) == (other.length, other.width, other.layer)

    def __hash__(self):
        # same fields as __eq__
        return hash((self.length, self.width, self.layer))

    def build(self) -> gf.Component:
        return RegularArmConfig.regularArm(
        self.length, 
        self.width, 
        self.layer, 
        self.CONNECTION_PORT_NAME, 
        self.GAP_PORT_NAME
    )

    
    @gf.cell
    @staticmethod
    def regularArm(length: float, width: float, layer, connect_port_name: str, gap_port_name: str) -> gf.Component:
        c = gf.Component()
        c.add_polygon([(0, 0), (length, 0), (length, width), (0, width)], layer=layer)
        c.add_port(name=connect_port_name, center=(length, width / 2), width=width, orientation=0, layer=layer, port_type="electrical")
        c.add_port(name=gap_port_name, center=(0, width / 2), width=width, orientation=180, layer=layer, port_type="electrical")
        return c

    def total_length(self) -> float:
        """
        Returns the total length of the arm.
        This method returns the length of the arm.
        """
        return self.length
    
    def validate(self) -> None:
        super().validate()
        if self.length <= 0:
            raise ValueError("Length must be positive.")
        if self.width <= 0:
            raise ValueError("Width must be positive.")