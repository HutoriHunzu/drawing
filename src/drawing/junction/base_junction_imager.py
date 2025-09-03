from gdsfactory.typings import LayerSpec
from ..shared import JUNCTION_PICTURE_LAYER
from ..base_config import BaseConfig

class BaseJunctionImager(BaseConfig):
    layer: LayerSpec = JUNCTION_PICTURE_LAYER