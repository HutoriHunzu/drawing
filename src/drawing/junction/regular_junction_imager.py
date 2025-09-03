from .base_junction_imager import BaseJunctionImager
import gdsfactory as gf

class RegularJunctionImager(BaseJunctionImager):
    """
    Configuration for the area to take image of a junction 
    Attributes:
        layer (LayerSpec): Layer specification for for future scripts to know where to take the image.
        length (float): Length of the area.
        width (float): Width of the area.
    """
    length: float = 140
    width: float = 93

    # 140 width
    # 93 height 

    # 100x microscope window
    
    def build(self) -> gf.Component:
        return RegularJunctionImager.regularJunctionImager(
        self.length, 
        self.width, 
        self.layer
    )

    
    @gf.cell
    @staticmethod
    def regularJunctionImager(length: float, width: float, layer: gf.typings.LayerSpec) -> gf.Component:
        c = gf.Component()
        c << gf.components.rectangle(size=(length, width), layer=layer)
        return c
    
    def validate(self) -> None:
        super().validate()
        if self.length <= 0:
            raise ValueError("Length must be positive.")
        if self.width <= 0:
            raise ValueError("Width must be positive.")