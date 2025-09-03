
from ..base_config import BaseConfig
import gdsfactory as gf

class BaseResonatorConfig(BaseConfig):
    """
    Base configuration for resonator components.
    Attributes:
        layer (LayerSpec): Layer specification for the resonator component.
    """
    
    def build(self) -> gf.Component:
        raise NotImplementedError("Subclasses should implement this method.")

    def validate(self) -> None:
        pass