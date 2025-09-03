import gdsfactory as gf
import gdsfactory.components as gc
from pydantic import ConfigDict, computed_field, model_validator
from pyparsing import cached_property
from .base_arm import BaseArmConfig

class FunnelrArmConfig(BaseArmConfig):
    """
    Configuration for a funnel-shaped arm component.
    Attributes:
        layer (LayerSpec): Layer specification for the funnel arm component.
        wide_length (float): Length of the wide part of the funnel.
        wide_width (float): Width of the wide part of the funnel.
        narrow_length (float): Length of the narrow part of the funnel.
        narrow_width (float): Width of the narrow part of the funnel.
    """

    wide_length: float = 10.0
    wide_width: float = 5.0
    narrow_length: float = 10.0
    narrow_width: float = 2.0

    def __eq__(self, other):
        if not isinstance(other, FunnelrArmConfig):
            return NotImplemented
        # include layer if it affects build
        return (self.wide_length, self.wide_width, self.narrow_length, self.narrow_width, self.layer) == (other.wide_length, other.wide_width, other.narrow_length, other.narrow_width, other.layer)

    def __hash__(self):
        # same fields as __eq__
        return hash((self.wide_length, self.wide_width, self.narrow_length, self.narrow_width, self.layer))

    def build(self) -> gf.Component:
        return FunnelrArmConfig._build(
            self.wide_length,
            self.wide_width,
            self.narrow_length,
            self.narrow_width,
            self.layer,
        )

    @gf.cell
    @staticmethod
    def funnelrArm(
        wide_length: float,
        wide_width: float,
        narrow_length: float,
        narrow_width: float,
        layer,
    ) -> gf.Component:
        c = gf.Component()
        
        # Create the trapezoidal and rectangular shapes
        # Trapezoid: wide at the top, narrow at the bottom
        tripozoid = gf.Component()
        tripozoid.add_polygon([(0,wide_width/2), (wide_length, narrow_width/2), (wide_length, -narrow_width/2), (0,-wide_width/2)], layer=layer)
        tripozoid.add_port(name="connection", center=(0, tripozoid.center[1]/2), width=wide_width, orientation=180, layer=layer, port_type="electrical")

        # Rectangle: narrow at the top, wide at the bottom
        # Note: The rectangle is positioned to the right of the trapezoid
        rectangle = gf.Component()
        rectangle.add_polygon([(0, 0), (narrow_length, 0), (narrow_length, narrow_width), (0, narrow_width)], layer=layer)
        rectangle.add_port(name="gap", center=(narrow_length, narrow_width / 2), width=narrow_width, orientation=0, layer=layer, port_type="electrical")

        t_ref = c << tripozoid.move((-wide_length, narrow_width/2))
        r_ref = c << rectangle

        c.add_ports(t_ref.ports)
        c.add_ports(r_ref.ports)

        c.flatten()

        return c.mirror_x()

    def total_length(self) -> float:
        """
        Returns the total length of the arm.
        This method returns the length of the arm.
        """
        return self.narrow_length + self.wide_length

    @model_validator(mode='after')
    def validate(self) -> None:
        super().validate()
        if self.wide_length <= 0:
            raise ValueError("Wide length must be positive.")
        if self.wide_width <= 0:
            raise ValueError("Wide width must be positive.")
        if self.narrow_length <= 0:
            raise ValueError("Narrow length must be positive.")
        if self.narrow_width <= 0:
            raise ValueError("Narrow width must be positive.")
        if self.wide_width <= self.narrow_width:
            raise ValueError("Wide width must be greater than narrow width.")