from drawing.junction.base_junction import BaseJunctionConfig
from drawing.meander.euler import meander_euler
from drawing.resonator.base_resonator import BaseResonatorConfig
from drawing.resonator.meander_resonator import MeanderResonatorConfig
from drawing.transmon.transmon import TransmonConfig
from .base_sample import BaseSampleConfig
import gdsfactory as gf

class twoResonatorsTwoTransmonSampleConfig(BaseSampleConfig):
    """
    Configuration for a sample with two resonators and two transmons.
    Attributes:
        transmon (TransmonConfig): Configuration for the transmon.
        transmonAntenna (TransmonConfig): Configuration for the transmon antenna.
        ResonatorLeft (BaseResonatorConfig): Configuration for the left resonator.
        ResonatorRight (BaseResonatorConfig): Configuration for the right resonator.
    """

    transmon : TransmonConfig = TransmonConfig()
    transmonAntenna : TransmonConfig = TransmonConfig()

    ResonatorLeft : BaseResonatorConfig = MeanderResonatorConfig()
    ResonatorRight : BaseResonatorConfig = MeanderResonatorConfig()

    def build(self) -> gf.Component:
        return twoResonatorsTwoTransmonSampleConfig.twoResonatorsTwoTransmonSample(
            transmon=self.transmon.build(),
            transmonAntenna=self.transmonAntenna.build(),
            ResonatorLeft=self.ResonatorLeft.build(),
            ResonatorRight=self.ResonatorRight.build()
        )

    @staticmethod
    @gf.cell
    def twoResonatorsTwoTransmonSample(transmon : gf.Component, transmonAntenna : gf.Component, ResonatorLeft : gf.Component, ResonatorRight : gf.Component) -> gf.Component:
        c = gf.Component()

        res = meander_euler(wire_width = 100,
        height = 1025,
        padding_length = 2400,
        spacing = 300,
        num_turns = 6,
        radius = 100)

        res_left_ref = c << res.copy()
        res_right_ref = c << res.copy()

        # res_left_ref = c << ResonatorLeft
        # res_right_ref = c << ResonatorRight

        res_right_ref.movex(res_left_ref.xmax - res_right_ref.xmin + 3500)

        transmon_ref = c << transmon
        transmon_antenna_ref = c << transmonAntenna

        transmon_ref.movex(res_right_ref.xmax - transmon_ref.xmin + 400)

        transmon_antenna_ref.movex(transmon_ref.xmax - transmon_antenna_ref.xmin + 300)

        return c


    def get_jopherson_junctions(self) -> list[BaseJunctionConfig]:
        return [self.transmon.junction, self.transmonAntenna.junction]