from ..base_config import BaseConfig
import gdsfactory as gf
from .base_cut_indicator import BaseCutIndicatorConfig

class UniformCutIndicatorConfig(BaseCutIndicatorConfig):
    """Configuration for a uniform cut indicator.

    Attributes:
        floors (int): Number of floors/steps in the indicator.
        last_floor_length (float): Length of the last floor/step.
        layer (LayerSpec): Layer specification for the junction component.
    """
    floors: int = 6
    last_floor_length: float = 50

    def build(self) -> gf.Component:
        return UniformCutIndicatorConfig.uniformCutIndicator(
            length=self.length,
            width=self.width,
            gap=self.gap,
            layer=self.layer,
            floors=self.floors,
            floor_length=self.floor_length,
            bounder_length=self.bounder_length
        )

    @staticmethod
    @gf.cell
    def uniformCutIndicator(
        length: float,
        width: float,
        gap: float,
        layer: gf.typings.LayerSpec,
        floors: int,
        floor_length: float,
        bounder_length: float
    ) -> gf.Component:
        c = gf.Component()

        bounder_length = (length - gap) / 2
        floor_width = width / floors

        c << gf.components.rectangle(size=(bounder_length, floor_width), layer=layer)

        for i in range(floors):
            rec_ref = c << gf.components.rectangle(size=(bounder_length - floor_length*i, floor_width), layer=layer)
            rec_ref.movey(floor_width*i)

        c_mirror_ref = c << c.copy().mirror_x()

        c_mirror_ref.movex(length + gap)

        c.flatten()

        return c

    @property
    def bounder_length(self) -> float:
        return (self.length - self.gap) / 2
    
    @property
    def floor_length(self) -> float:
        return (self.bounder_length - self.last_floor_length) / self.floors

    def validate(self) -> None:
        super()
        if self.floors < 0:
            raise ValueError(
                "Uniform Cut Indicator Config floors be greater than or equal to zero."
            )
        if self.gap < 0:
            raise ValueError(
                "Uniform Cut Indicator Config last floor width be greater than or equal to zero."
            )
        if self.bounder_length < 0:
            raise ValueError(
                "Uniform Cut Indicator Config length be greater than or equal to gap."
            )
        if self.bounder_length < 0:
            raise ValueError(
                "Uniform Cut Indicator Config length be greater than or equal to gap + last floor length."
            )