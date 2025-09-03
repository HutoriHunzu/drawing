from drawing.junction.base_junction import BaseJunctionConfig
from drawing.shared.utilities import SAMPLE_AREA_INDICATOR_LAYER
from pydantic import Field
from ..base_config import BaseConfig
import gdsfactory as gf

class BaseSampleConfig(BaseConfig):
    """
    Base configuration for sample components.
    Attributes:
        layer (LayerSpec): Layer specification for the sample.
        length (float): Length of the sample area.
        width (float): Width of the sample area.
        layer_area_indicator (LayerSpec): Layer specification for the area indicator.
    """
    length: float = 0
    width: float = 0
    
    layer_area_indicator : gf.typings.LayerSpec = Field(SAMPLE_AREA_INDICATOR_LAYER, exclude=True)

    def get_jopherson_junctions(self) -> list[BaseJunctionConfig]:
        return []