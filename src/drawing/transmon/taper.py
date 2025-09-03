from pydantic import ConfigDict, Field, computed_field
from pyparsing import cached_property
from ..base_config import BaseConfig
import gdsfactory as gf


class TaperConfig(BaseConfig):
    """
    """
    length: float = 10
    wide_width: float = 5
    narrow_width: float = 1

    WIDE_CONNECTING_PORT_NAME: str = Field("wide_connection", exclude=True)
    NARROW_CONNECTING_PORT_NAME: str = Field("narrow_connection", exclude=True)

    model_config = ConfigDict(frozen=True)

    def build(self) -> gf.Component:
        return TaperConfig.taper(
            length=self.length,
            wide_width=self.wide_width,
            narrow_width=self.narrow_width,
            layer=self.layer,
            wide_port_name=self.WIDE_CONNECTING_PORT_NAME,
            narrow_port_name=self.NARROW_CONNECTING_PORT_NAME,
        )

    @staticmethod
    @gf.cell
    def taper(
        length: float,
        wide_width: float,
        narrow_width: float,
        layer: tuple[int, int],
        wide_port_name: str,
        narrow_port_name: str,
    ) -> gf.Component:
        c = gf.Component()

        c.add_polygon([(0,wide_width/2), (length, narrow_width/2), (length, -narrow_width/2), (0,-wide_width/2)], layer=layer)
        
        # Add ports for connecting to pad and junction
        c.add_port(name=wide_port_name, center=(0, 0), width=wide_width, orientation=180, layer=layer, port_type="electrical")
        c.add_port(name=narrow_port_name, center=(length, 0), width=narrow_width, orientation=0, layer=layer, port_type="electrical")
        
        # Taper + Compass connected
        return c

    def validate(self):
        """
        Validates the taper configuration.

        This method checks if the configuration parameters are valid.
        """
        if self.length <= 0 or self.wide_width <= 0 or self.narrow_width <= 0:
            raise ValueError(
                "Taper length and widths must be positive values."
            )
        if self.wide_width < self.narrow_width:
            raise ValueError(
                "Wide width must be greater than or equal to narrow width."
            )