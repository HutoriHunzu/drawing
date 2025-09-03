import gdsfactory as gf
from .base_arm import BaseArmConfig

class TArmConfig(BaseArmConfig):
    """
    TArmConfig defines the configuration for a T-shaped arm component.
    Attributes:
        horizontal_length (float): Length of the horizontal section of the T-arm. Default is 10.0.
        horizontal_width (float): Width of the horizontal section of the T-arm. Default is 1.0.
        vertical_length (float): Length of the vertical section of the T-arm. Default is 1.0.
        vertical_width (float): Width of the vertical section of the T-arm. Default is 10.0.
        layer (LayerSpec): Layer specification for the junction component.
    """

    horizontal_length: float = 10.0
    horizontal_width: float = 1.0
    vertical_length: float = 1.0
    vertical_width: float = 10.0

    def __eq__(self, other):
        if not isinstance(other, TArmConfig):
            return NotImplemented
        # include layer if it affects build
        return (self.horizontal_length, self.horizontal_width, self.vertical_length ,self.vertical_width, self.layer) == (other.horizontal_length, other.horizontal_width, other.vertical_length ,other.vertical_width, other.layer)

    def __hash__(self):
        # same fields as __eq__
        return hash((self.horizontal_length, self.horizontal_width, self.vertical_length ,self.vertical_width, self.layer))

    def build(self) -> gf.Component:
        return TArmConfig.tArm(
        self.horizontal_length, 
        self.horizontal_width, 
        self.vertical_length, 
        self.vertical_width,
        self.layer, 
        self.CONNECTION_PORT_NAME, 
        self.GAP_PORT_NAME
    )

    
    @gf.cell
    @staticmethod
    def tArm(horizontal_length: float,
            horizontal_width: float,
            vertical_length: float,
            vertical_width: float,
            layer: gf.typings.LayerSpec,
            connect_port_name: str,
            gap_port_name: str
        ) -> gf.Component:
        c = gf.Component()
        c.add_polygon([(0, 0), (horizontal_length, 0), (horizontal_length, horizontal_width), (0, horizontal_width), (0, -vertical_width/2), (-vertical_length, -vertical_width/2), (-vertical_length, vertical_width/2), (0, vertical_width/2)], layer=layer)
        c.add_port(name=connect_port_name, center=(horizontal_length, horizontal_width / 2), width=horizontal_width, orientation=0, layer=layer, port_type="electrical")
        c.add_port(name=gap_port_name, center=(0, horizontal_width / 2), width=horizontal_width, orientation=180, layer=layer, port_type="electrical")

        c.flatten()

        return c

    def total_length(self) -> float:
        """
        Returns the total length of the arm.
        This method returns the length of the arm.
        """
        return self.horizontal_length + self.vertical_length
    
    def validate(self) -> None:
        super().validate()
        if self.horizontal_length <= 0:
            raise ValueError("Horizontal length must be positive.")
        if self.horizontal_width <= 0:
            raise ValueError("Horizontal width must be positive.")
        if self.vertical_length <= 0:
            raise ValueError("Vertical length must be positive.")
        if self.vertical_width <= 0:
            raise ValueError("Vertical width must be positive.")