import gdsfactory.components as gc
import gdsfactory as gf
from pydantic import ConfigDict, Field
from ..base_config import BaseConfig
import gdsfactory as gf

class AntennaConfig(BaseConfig):
    """
    Configuration for building an antenna component in a transmon layout.

    This configuration defines the dimensions and layer for the antenna. The antenna
    consists of a rectangular (compass) part and a circular part, which are connected
    to form the final shape.

    Attributes:
        length (float): Length of the rectangular part.
        width (float): Width of the rectangular part.
        radius (float): Radius of the circular part.
        layer (LayerSpec): GDS layer specification for the antenna.
    """
    length: float = 140
    width: float = 10
    radius: float = 25
    
    ANTENNA_START_PORT: str = Field('start', exclude=True)

    model_config = ConfigDict(frozen=True)

    def build(self) -> gf.Component:
        return AntennaConfig.antenna(
            length=self.length,
            width=self.width,
            radius=self.radius,
            layer=self.layer,
            start_port_name=self.ANTENNA_START_PORT,
        )

    @staticmethod
    @gf.cell
    def antenna(
        length: float,
        width: float,
        radius: float,
        layer: tuple[int, int],
        start_port_name: str,
    ) -> gf.Component:
        c = gf.Component()

        # Rectangular pad (compass shape)
        compass = gc.compass(size=(length, width), layer=layer)
        circle = gc.circle(radius=radius, layer=layer).copy()

        circle.add_port(
            name="center",
            center=circle.center,
            width=width,
            orientation=180,
            layer=layer
        )

        compass_ref = c.add_ref(compass)
        circle_ref = c.add_ref(circle)

        # Connect the circle to the east port of the compass (e3)
        compass_ref.connect("e3", circle_ref.ports["center"], allow_type_mismatch=True, allow_width_mismatch=True)

        # Add main antenna port at the west end of the compass (e1)
        c.add_port(start_port_name, port=compass_ref.ports["e1"])

        c.flatten()

        return c

    def validate(self) -> None:
        """
        Validates the antenna configuration.

        Raises:
            ValueError: If the antenna length, width, or radius is non-positive.
            TypeError: If the layer is not of type LayerSpec.
        """
        if self.length <= 0 or self.width <= 0 or self.radius <= 0:
            raise ValueError("Antenna dimensions must be positive.")