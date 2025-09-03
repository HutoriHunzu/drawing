from drawing.base_config import BaseConfig
import gdsfactory as gf
from ..junction import BaseJunctionConfig, SymmetricJunctionConfig
from pydantic import ConfigDict

class SquidConfig(BaseConfig):
    """Configuration for a squid component.
    Attributes:
        flux_hole_width (float): Width of the flux hole.
        flux_hole_length (float): Length of the flux hole.
        flux_hole_bar_length (float): Length of the flux hole bar.
        top_junction (BaseJunctionConfig): Configuration for the top junction.
        bottom_junction (BaseJunctionConfig): Configuration for the bottom junction.
    """
    flux_hole_width: float = 5
    flux_hole_length: float = 10

    flux_hole_bar_length: float = 5

    top_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    bottom_junction: BaseJunctionConfig = SymmetricJunctionConfig()

    LEFT_CONNECTING_PORT_NAME: str = "left_connection"
    RIGHT_CONNECTING_PORT_NAME: str = "right_connection"

    model_config = ConfigDict(frozen=True)

    def build(self) -> gf.Component:
        return SquidConfig.squid(
            flux_hole_width=self.flux_hole_width,
            flux_hole_length=self.flux_hole_length,
            flux_hole_bar_length=self.flux_hole_bar_length,
            top_junction=self.top_junction.build().copy(),
            bottom_junction=self.bottom_junction.build().copy(),
            left_port_name=self.LEFT_CONNECTING_PORT_NAME,
            right_port_name=self.RIGHT_CONNECTING_PORT_NAME,
            layer=self.layer,
            top_junction_left_connecting_port=self.top_junction.LEFT_CONNECTING_PORT_NAME,
            top_junction_right_connecting_port=self.top_junction.RIGHT_CONNECTING_PORT_NAME,
            bottom_junction_left_connecting_port=self.bottom_junction.LEFT_CONNECTING_PORT_NAME,
            bottom_junction_right_connecting_port=self.bottom_junction.RIGHT_CONNECTING_PORT_NAME
        )

    @gf.cell
    @staticmethod
    def squid(
        flux_hole_width: float,
        flux_hole_length: float,
        flux_hole_bar_length: float,
        top_junction: gf.Component,
        bottom_junction: gf.Component,
        left_port_name: str,
        right_port_name: str,
        layer,
        top_junction_right_connecting_port: str,
        top_junction_left_connecting_port: str,
        bottom_junction_right_connecting_port: str,
        bottom_junction_left_connecting_port: str,
    ) -> gf.Component:
        c = gf.Component()
        """
        Builds the squid component by creating the flux hole and junctions.
        Returns:
            gf.Component: The squid component.
        """
        c: gf.Component = gf.Component()

        # Create the flux hole
        tj_ref = c << top_junction
        bj_ref = c << bottom_junction
        bj_ref.movey(- flux_hole_width)

        # Create the flux hole rectangle
        flux_hole_bar_width = tj_ref.ymax - bj_ref.ymin
        top_junction_y_length = tj_ref.ymax - tj_ref.ymin
        bottom_junction_y_length = bj_ref.ymax - bj_ref.ymin
        flux_hole_bar_left = gf.Component()
        flux_hole_bar_left.add_polygon([(0, 0), (flux_hole_bar_length, 0), (flux_hole_bar_length, flux_hole_bar_width), (0, flux_hole_bar_width)], layer=layer)
        flux_hole_bar_left.add_port(name="connect_top", center=(flux_hole_bar_length, flux_hole_bar_left.ymax - top_junction_y_length / 2), width=top_junction_y_length, orientation=0, layer=layer, port_type="electrical")
        flux_hole_bar_left.add_port(name="connect_bottom", center=(flux_hole_bar_length, flux_hole_bar_left.ymin + bottom_junction_y_length / 2), width=bottom_junction_y_length, orientation=0, layer=layer, port_type="electrical")

        flux_hole_bar_right = flux_hole_bar_left.copy().mirror_x()

        fhb_left = c << flux_hole_bar_left
        fhb_right = c << flux_hole_bar_right

        fhb_left.connect("connect_top", tj_ref.ports[top_junction_left_connecting_port])
        fhb_left.connect("connect_bottom", bj_ref.ports[bottom_junction_left_connecting_port])

        fhb_right.connect("connect_top", tj_ref.ports[top_junction_right_connecting_port])
        fhb_right.connect("connect_bottom", bj_ref.ports[bottom_junction_right_connecting_port])
        
        c.add_port(name=left_port_name, center=(c.xmin, c.center[1]), width=flux_hole_bar_width, orientation=180, layer=layer, port_type="electrical")
        c.add_port(name=right_port_name, center=(c.xmax, c.center[1]), width=flux_hole_bar_width, orientation=0, layer=layer, port_type="electrical")

        c.flatten()

        return c

    def get_jopherson_junctions(self) -> list[BaseJunctionConfig]:
        return [self.top_junction, self.bottom_junction]

    def validate(self) -> None:
        super().validate()
        self.top_junction.validate()
        self.bottom_junction.validate()
        if self.flux_hole_width <= 0:
            raise ValueError("Flux hole width must be positive.")
        if self.flux_hole_length <= 0:
            raise ValueError("Flux hole length must be positive.")
        if self.flux_hole_bar_length <= 0:
            raise ValueError("Flux hole bar length must be positive.")
        if self.top_junction.total_length() != self.bottom_junction.total_length():
            raise ValueError("Top and bottom junctions must have the same total length including gaps.")