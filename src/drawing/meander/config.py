"""
Configuration objects for meander components.

Provides Pydantic models to encapsulate parameters for both Euler and optimal turn
meander implementations.
"""
from typing import Literal
from pydantic import BaseModel
from gdsfactory.typings import LayerSpec
from src.drawing.shared.utilities import DEFAULT_LAYER


class MeanderEulerConfig(BaseModel):
    """
    Configuration for creating a meander pattern using Euler bends.

    Attributes:
        type (str): Identifier for the Euler meander configuration.
        wire_width (float): Width of the wire.
        height (float): Total height of the meander.
        padding_length (float): Padding length at the start/end.
        spacing (float): Horizontal spacing between turns.
        num_turns (int): Number of turns.
        radius (float): Radius used in the Euler bends.
        layer (LayerSpec): GDS layer specification.
    """
    type: Literal['meander_euler'] = "meander_euler"
    wire_width: float = 0.2
    height: float = 10.0
    padding_length: float = 3.0
    spacing: float = 5.0
    num_turns: int = 9
    radius: float = 1.0
    layer: LayerSpec = DEFAULT_LAYER


class MeanderOptimalTurnConfig(BaseModel):
    """
    Configuration for creating a meander pattern using optimal 90-degree turns.

    Attributes:
        type (str): Identifier for the optimal turn meander configuration.
        wire_width (float): Width of the wire.
        height (float): Total height of the meander.
        padding_length (float): Padding length at the start/end.
        spacing (float): Horizontal spacing between turns.
        num_turns (int): Number of turns.
    """
    type: Literal['meander_optimal_turn'] = "meander_optimal_turn"
    wire_width: float = 0.2
    height: float = 10.0
    padding_length: float = 3.0
    spacing: float = 2.0
    num_turns: int = 9
