from drawing.shared.utilities import JUNCTION_PICTURE_LAYER
import gdsfactory as gf
from .base_junction import BaseJunctionConfig
from .base_arm import BaseArmConfig
from .regular_arm import RegularArmConfig
from pydantic import ConfigDict

class SymmetricJunctionConfig(BaseJunctionConfig):
    """
    Configuration for symmetric junction components.
    Attributes:
        arm (BaseArmConfig): Configuration for the arm component.
        gap_length (float): Length of the gap between the arms.
        layer (LayerSpec): Layer specification for the junction component.
        gap_layer (LayerSpec): Layer specification for the gap.
        gap_create (bool): Whether to create a gap in the junction.
    """

    arm: BaseArmConfig = RegularArmConfig()

    model_config = ConfigDict(frozen=True)

    @property
    def LEFT_CONNECTING_PORT_NAME(self) -> str:
        return self.LEFT_PREFIX + self.arm.CONNECTION_PORT_NAME
    
    @property
    def RIGHT_CONNECTING_PORT_NAME(self) -> str:
        return self.RIGHT_PREFIX + self.arm.CONNECTION_PORT_NAME

    def get_left_arm_config(self) -> BaseArmConfig:
        return self.arm

    def get_right_arm_config(self) -> BaseArmConfig:
        return self.arm

    def build(self) -> gf.Component:
        return SymmetricJunctionConfig.symmetricJunction(
            arm=self.arm.build().copy(),
            arm_gap_port_name=self.arm.GAP_PORT_NAME,
            gap_length=self.gap_length,
            layer=self.layer,
            gap_layer=self.gap_layer,
            gap_create=self.gap_create,
            right_prefix=self.RIGHT_PREFIX,
            left_prefix=self.LEFT_PREFIX,
        )
    
    @staticmethod
    @gf.cell
    def symmetricJunction(arm: gf.Component, arm_gap_port_name: str, gap_length: float, layer, gap_layer, gap_create: bool, right_prefix: str, left_prefix: str) -> gf.Component:
        c = gf.Component()

        arm.layer = layer

        # Create left and right arms using the same arm configuration
        # a = arm.build ()      

        right_arm_ref = c << arm.copy()
        left_arm_ref = c << arm.mirror_x()

        # Add validation that port "gap" exists in both arms

        # Connect the arms via ports
        left_arm_ref.connect(arm_gap_port_name, right_arm_ref.ports[arm_gap_port_name])
        # Position the right arm
        left_arm_ref.movex(-gap_length)

        if gap_create:
            # Create a gap in the junction
            gap = c << gf.components.rectangle(size=(gap_length, right_arm_ref.ymax - right_arm_ref.ymin), layer=gap_layer)
            gap.connect("e1", left_arm_ref.ports[arm_gap_port_name], allow_layer_mismatch=True)
            gap.connect("e2", right_arm_ref.ports[arm_gap_port_name], allow_layer_mismatch=True)

        # Add ports for the arms
        c.add_ports(right_arm_ref.ports, prefix=right_prefix)
        c.add_ports(left_arm_ref.ports, prefix=left_prefix)

        return c

    def total_length(self) -> float:
        """
        Returns the total length of the junction.
        This method returns the total length of both arms plus the gap length.
        The total length is calculated as twice the arm length plus the gap length.
        """
        return self.arm.total_length() * 2 + self.gap_length
    
    def validate(self) -> None:
        if self.gap_length <= 0:
            raise ValueError("Gap length must be positive.")
        
        self.arm.validate()