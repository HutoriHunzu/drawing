from drawing.test_junctions.base_test_junctions import BaseTestJunctionsConfig
from drawing.transmon.transmon import TransmonConfig
import gdsfactory as gf

class FiveTestJunctionsConfig(BaseTestJunctionsConfig):
    
    gap_start_length: float = 1.0
    gap_end_length: float = 5.0
    transmonConfig: TransmonConfig = TransmonConfig()

    def build(self) -> gf.Component:
        return FiveTestJunctionsConfig.fiveTestJunctionsConfig()
    
    @gf.cell
    @staticmethod
    def fiveTestJunctionsConfig() -> gf.Component:
        c = gf.Component()
        return c

    def getData(self) -> dict:
        # test junctions:
        #   type:
        #       DOLAN
        #       DOLATHAN
        #       MANHANTAN
        #    BRIDGE START GAP
        #    BRIDGE END GAP
        #    FINGER WIDTH
        rtn = {}
        rtn["type"] = self.transmonConfig.junction.junction_type
        rtn["BRIDGE START GAP"] = self.gap_start_length
        rtn["BRIDGE END GAP"] = self.gap_end_length
        leftFinger = self.transmonConfig.junction.get_left_arm_config().to_json()
        print(leftFinger)
        rtn["LEFT FINGER"] = leftFinger
        rightFinger = self.transmonConfig.junction.get_right_arm_config().to_json()
        print(rightFinger)
        rtn["RIGHT FINGER"] = rightFinger
        return rtn

    def validate(self) -> None:
        pass