from pydantic import ConfigDict, Field
from ..base_config import BaseConfig
import gdsfactory as gf
from ..shared import smooth_corners

class PadConfig(BaseConfig):
    """

    Attributes:
        layer (LayerSpec): GDS layer specification.
    """
    width: float = 50
    length: float = 20
    radius: float = 5

    LEFT_CONNECTING_PORT_NAME: str = Field("left_connection", exclude=True)
    RIGHT_CONNECTING_PORT_NAME: str =  Field("right_connection", exclude=True)

    model_config = ConfigDict(frozen=True)

    def build(self) -> gf.Component:
        return PadConfig.pad(
            width=self.width,
            length=self.length,
            radius=self.radius,
            layer=self.layer,
            left_port_name=self.LEFT_CONNECTING_PORT_NAME,
            right_port_name=self.RIGHT_CONNECTING_PORT_NAME,
        )

    @staticmethod
    @gf.cell
    def pad(
        width: float,
        length: float,
        radius: float,
        layer: tuple[int, int],
        left_port_name: str,
        right_port_name: str,
    ) -> gf.Component:
        c = gf.Component()
        """
        Builds pad components and integrates them into the given component.

        The method creates two pads (left and right), applies optional corner rounding,
        and sets up electrical ports.
        """
        c = gf.Component()
        c.add_polygon([(0, 0), (length, 0), (length, width), (0, width)], layer=layer)

        c.add_port(name=left_port_name, center=(0, width / 2), width=width, orientation=180, layer=layer, port_type="electrical")
        c.add_port(name=right_port_name, center=(length, width / 2), width=width, orientation=0, layer=layer, port_type="electrical")

        if radius > 0:
            c = smooth_corners(c, radius=radius, layer=layer)

        return c

    def validate(self) -> None:
        """
        Validates the pad configuration.

        Raises:
            ValueError: If the pad width or height is non-positive.
            TypeError: If the layer is not of type LayerSpec.
        """
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Pad width and height must be positive.")