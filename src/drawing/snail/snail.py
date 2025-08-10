from drawing.base_config import BaseConfig
from drawing.junction.regular_arm import RegularArmConfig
import gdsfactory as gf
from ..junction import BaseJunctionConfig, SymmetricJunctionConfig
from pydantic import computed_field
from pyparsing import cached_property

class SnailConfig(BaseConfig):
    """Configuration for a squid component.
    Attributes:
        flux_hole_width (float): Width of the flux hole.
        flux_hole_length (float): Length of the flux hole.
        flux_hole_bar_length (float): Length of the flux hole bar.
        top_junction (BaseJunctionConfig): Configuration for the top junction.
        top_middle_junction (BaseJunctionConfig): Configuration for the middle top junction.
        top_right_junction (BaseJunctionConfig): Configuration for the right top junction.
        bottom_junction (BaseJunctionConfig): Configuration for the bottom junction.
    """
    flux_hole_width: float = 5
    flux_hole_length: float = 10

    flux_hole_bar_length: float = 5

    top_left_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    top_middle_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    top_right_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    bottom_junction: BaseJunctionConfig = SymmetricJunctionConfig(
        arm = RegularArmConfig(
                length = ( SymmetricJunctionConfig().total_length() * 3 - 1 ) / 2
            )
        )

    @computed_field
    @cached_property
    def build(self) -> gf.Component:
        """
        Builds the squid component by creating the flux hole and junctions.
        Returns:
            gf.Component: The squid component.
        """
        c: gf.Component = gf.Component()

        
        c_top_left_junction = self.top_left_junction.build
        c_top_middle_junction = self.top_middle_junction.build
        c_top_right_junction = self.top_right_junction.build
        c_bottom_junction = self.bottom_junction.build

        c_top_left_junction_ref = c << c_top_left_junction
        c_top_middle_junction_ref = c << c_top_middle_junction
        c_top_right_junction_ref = c << c_top_right_junction
        c_bottom_junction_ref = c << c_bottom_junction

        

        c_top_left_junction_ref.connect(self.top_left_junction.RIGHT_CONNECTING_PORT_NAME,
                                        c_top_middle_junction_ref.ports[self.top_left_junction.LEFT_CONNECTING_PORT_NAME])
        c_top_right_junction_ref.connect(self.top_left_junction.LEFT_CONNECTING_PORT_NAME,
                                         c_top_middle_junction_ref.ports[self.top_left_junction.RIGHT_CONNECTING_PORT_NAME])

        c_bottom_junction_ref.movey(- self.flux_hole_width)

        flux_hole_bar_width = c.ymax - c.ymin
        top_junction_y_length = c_top_left_junction_ref.ymax - c_top_left_junction_ref.ymin
        bottom_junction_y_length = c_bottom_junction.ymax - c_bottom_junction.ymin
        flux_hole_bar_left = gf.Component()
        flux_hole_bar_left.add_polygon([(0, 0), (self.flux_hole_bar_length, 0), (self.flux_hole_bar_length, flux_hole_bar_width), (0, flux_hole_bar_width)], layer=self.layer)
        flux_hole_bar_left.add_port(name="connect_top", center=(self.flux_hole_bar_length, flux_hole_bar_left.ymax - top_junction_y_length / 2), width=top_junction_y_length, orientation=0, layer=self.layer, port_type="electrical")
        flux_hole_bar_left.add_port(name="connect_bottom", center=(self.flux_hole_bar_length, flux_hole_bar_left.ymin + bottom_junction_y_length / 2), width=bottom_junction_y_length, orientation=0, layer=self.layer, port_type="electrical")

        flux_hole_bar_right = flux_hole_bar_left.copy().mirror_x()

        fhb_left = c << flux_hole_bar_left
        fhb_right = c << flux_hole_bar_right

        fhb_left.connect("connect_top", c_top_left_junction_ref.ports["left_connection"])
        fhb_left.connect("connect_bottom", c_bottom_junction_ref.ports["left_connection"])

        fhb_right.connect("connect_top", c_top_left_junction_ref.ports["right_connection"])
        fhb_right.connect("connect_bottom", c_bottom_junction_ref.ports["right_connection"])

        c.flatten()

        return c

    @staticmethod
    def bottom_junction_length_arm_length(left_junction: BaseJunctionConfig = SymmetricJunctionConfig(), middle_junction: BaseJunctionConfig = SymmetricJunctionConfig(), right_junction: BaseJunctionConfig = SymmetricJunctionConfig(), bottom_gap: float = 1) -> float:
        """Calculates the length of the bottom junction arm.
        Args:
            left_junction (BaseJunctionConfig): Configuration for the left junction.
            middle_junction (BaseJunctionConfig): Configuration for the middle junction.
            right_junction (BaseJunctionConfig): Configuration for the right junction.
            bottom_gap (float): Gap between the bottom junction and the flux hole.
        Returns:
            float: The length of the bottom junction arm.
        """
        return ( left_junction.total_length() + middle_junction.total_length() + right_junction.total_length() - bottom_gap ) / 2

    def bottom_junction_length_arm_length(self) -> float:
        """Calculates the length of the bottom junction arm based on the current configuration.
        Returns:
            float: The length of the bottom junction arm.
        """
        return SnailConfig.bottom_junction_length_arm_length(
            left_junction=self.top_left_junction,
            middle_junction=self.top_middle_junction,
            right_junction=self.top_right_junction,
            bottom_gap=self.flux_hole_width
        )

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
        if self.top_left_junction.total_length() +  self.top_middle_junction.total_length() +  self.top_right_junction.total_length() != self.bottom_junction.total_length():
            raise ValueError("The total length of the top junctions must equal the length of the bottom junction.")