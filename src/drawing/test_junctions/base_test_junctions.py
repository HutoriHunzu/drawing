from ..base_config import BaseConfig
import gdsfactory as gf

class BaseTestJunctionsConfig(BaseConfig):
    def build(self) -> gf.Component:
        raise NotImplementedError("Subclasses should implement this method.")
    
    def getData(self) -> list:
        raise NotImplementedError("Subclasses should implement this method.")

    def validate(self) -> None:
        pass