from drawing.shared.utilities import DEFAULT_LAYER
from . wafer import WaferConfig
import gdsfactory as gf

class WaferRegularSplitConfig(WaferConfig):

    split_layer: gf.typings.LayerSpec = DEFAULT_LAYER
    vertical_split_length_in_raduis: float = 0.3
    vertical_split_y_position_in_raduis: float = 0.6
    horizontal_split_length_in_raduis: float = 1
    horizontal_split_y_position_in_raduis: float = 0.5
    horizontal_split_x_position_in_raduis: float = 0.5

    def build(self) -> gf.Component:
        return WaferRegularSplitConfig.waferRegularSplit(
            wafer=super().build().copy(), # Get the wafer
            split_layer=self.split_layer,
            vertical_split_length=self.vertical_split_length,
            vertical_split_y_position=self.vertical_split_y_position,
            horizontal_split_length=self.horizontal_split_length,
            horizontal_split_y_position=self.horizontal_split_y_position,
            horizontal_split_x_position=self.horizontal_split_x_position
        )

    @staticmethod
    @gf.cell
    def waferRegularSplit(
        wafer: gf.Component,
        split_layer: gf.typings.LayerSpec,
        vertical_split_length: float,
        vertical_split_y_position: float,
        horizontal_split_length: float,
        horizontal_split_y_position: float,
        horizontal_split_x_position: float,
    ) -> gf.Component:
        v_split_top_ref= wafer << gf.components.rectangle(size=(1, vertical_split_length), layer=split_layer)
        v_split_top_ref.movey(vertical_split_y_position)
        v_split_bottom_ref= wafer << gf.components.rectangle(size=(1, vertical_split_length), layer=split_layer)
        v_split_bottom_ref.movey(-(vertical_split_y_position + vertical_split_length))

        h_split_top_ref= wafer << gf.components.rectangle(size=(horizontal_split_length, 1), layer=split_layer)
        h_split_top_ref.movey(horizontal_split_y_position)
        h_split_top_ref.movex(-horizontal_split_x_position)

        h_split_top_ref= wafer << gf.components.rectangle(size=(horizontal_split_length, 1), layer=split_layer)
        h_split_top_ref.movey(-horizontal_split_y_position)
        h_split_top_ref.movex(-horizontal_split_x_position)


        return wafer
    
    @property
    def vertical_split_length(self):
        eff_r = self.radius
        if self.safe_layer != None:
            eff_r = self.safe_radius
        return self.vertical_split_length_in_raduis * eff_r
    
    @property
    def vertical_split_y_position(self):
        eff_r = self.radius
        if self.safe_layer != None:
            eff_r = self.safe_radius
        return self.vertical_split_y_position_in_raduis * eff_r
    
    @property
    def horizontal_split_length(self):
        eff_r = self.radius
        if self.safe_layer != None:
            eff_r = self.safe_radius
        return self.horizontal_split_length_in_raduis * eff_r
    
    @property
    def horizontal_split_y_position(self):
        eff_r = self.radius
        if self.safe_layer != None:
            eff_r = self.safe_radius
        return self.horizontal_split_y_position_in_raduis * eff_r
    
    @property
    def horizontal_split_x_position(self):
        eff_r = self.radius
        if self.safe_layer != None:
            eff_r = self.safe_radius
        return self.horizontal_split_x_position_in_raduis * eff_r


    def validate(self) -> None:
        if self.radius < 0:
            raise ValueError(
                "Wafer radius be greater than or equal to zero."
            )