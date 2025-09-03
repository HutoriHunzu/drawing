"""
Meander component implementations using Euler bends.

Provides functions to generate meander patterns with smooth curves using Euler
bends, suitable for high-performance GDS layouts.
"""

import gdsfactory as gf
import numpy as np
from itertools import chain
from gdsfactory.typings import LayerSpec
from ..shared.utilities import DEFAULT_LAYER, merge_decorator


@merge_decorator
def meander_euler(
    wire_width: float = 0.2,
    height: float = 10,
    padding_length: float = 3,
    spacing: float = 5,
    num_turns: int = 9,
    radius: float = 1,
    layer: LayerSpec = DEFAULT_LAYER,
) -> gf.Component:
    """
    Creates a meander pattern with Euler bends for smooth transitions.

    Args:
        wire_width (float): Width of the wire.
        height (float): Total height of the meander.
        padding_length (float): Straight section length at the start and end.
        spacing (float): Horizontal spacing between turns.
        num_turns (int): Number of turns in the meander.
        radius (float): Radius for the Euler bends.
        layer (LayerSpec): GDS layer specification.

    Returns:
        gf.Component: The generated meander component.
    """
    c = gf.Component()
    points = _generate_meander_points(
        height=height,
        padding_length=padding_length,
        spacing=spacing,
        num_turns=num_turns,
    )

    path = gf.path.smooth(
        points,
        radius=radius,
        bend=gf.path.euler,
        use_eff=True,
        npoints=720,
        p=1
    )
    cross_section = gf.cross_section.strip(width=wire_width, layer=layer)
    waveguide = gf.path.extrude(path, cross_section)

    c.add_ref(waveguide)
    start_port = gf.Port(
        'e1',
        center=tuple(points[0].tolist()),
        layer=layer[0],
        width=wire_width,
        orientation=180
    )
    end_port = gf.Port(
        'e2',
        center=tuple(points[-1].tolist()),
        layer=layer[0],
        width=wire_width,
        orientation=0
    )
    c.add_port('e1', port=start_port)
    c.add_port('e2', port=end_port)
    return c


def _generate_meander_points(
    height: float, padding_length: float, spacing: float, num_turns: int
) -> np.ndarray:
    """
    Generates a set of cumulative points for constructing a meander layout.

    Args:
        height (float): Total height of the meander.
        padding_length (float): Length of the padding at the start and end.
        spacing (float): Horizontal spacing between turns.
        num_turns (int): Number of turns.

    Returns:
        np.ndarray: Array of points representing the meander path.
    """
    step_up_edge = [0, height / 2]
    step_down_edge = [0, -height / 2]
    step_up = [0, height]
    step_down = [0, -height]
    step_horizontal = [spacing, 0]

    steps = (step_down, step_up)
    half_steps = (step_down_edge, step_up_edge)
    turn_points = list(chain(*[[steps[i % 2], step_horizontal] for i in range(num_turns)]))
    end_step = half_steps[num_turns % 2]
    total_points = (
        [[0, 0], [padding_length, 0], step_up_edge, step_horizontal] +
        turn_points +
        [end_step, [padding_length, 0]]
    )
    return np.array(total_points).cumsum(axis=0)
