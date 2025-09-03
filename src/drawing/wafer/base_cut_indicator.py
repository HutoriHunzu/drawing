from ..base_config import BaseConfig
import gdsfactory as gf

class BaseCutIndicatorConfig(BaseConfig):

    gap: float = 100
    width: float = 300
    length: float = 300

    def validate(self) -> None:
        if self.gap < 0:
            raise ValueError(
                "Base Cut Indicator Config gap be greater than or equal to zero."
            )
        if self.width < 0:
            raise ValueError(
                "Base Cut Indicator Config height be greater than or equal to zero."
            )
        if self.length < self.gap:
            raise ValueError(
                "Base Cut Indicator Config width be greater than or equal to gap."
            )