import gdsfactory as gf
import gdsfactory.components as gc
from ..shared import merge_decorator


@merge_decorator
@gf.cell
def meander_optimal_turn(
    wire_width: float = 0.2,
    height: float = 10,
    padding_length: float = 3,
    spacing: float = 2,
    num_turns: int = 9,
) -> gf.Component:
    """
    Creates a meander pattern using optimal 90-degree turns.

    Constructs a meander layout by combining padding sections, optimal turns, and
    spacing elements to generate a continuous path.

    Args:
        wire_width (float): Width of the meander wire.
        height (float): Total height of the meander.
        padding_length (float): Length of the padding sections.
        spacing (float): Spacing between turns.
        num_turns (int): Number of 90-degree turns.

    Returns:
        gf.Component: The complete meander component.
    """
    turn = gc.optimal_90deg(width=wire_width)
    turn_size = turn.xmax - turn.xmin

    padding_compass = gc.compass(size=(padding_length, wire_width))
    spacing_compass = gc.compass(size=(spacing, wire_width))
    height_compass = gc.compass(size=(height - 2 * turn_size, wire_width))
    padding_height_compass = gc.compass(size=(height / 2 - 2 * turn_size, wire_width))

    c = gf.Component()
    start_wg = c << padding_compass
    prev_port = start_wg.ports["e3"]

    ref = c << turn
    ref.connect("e1", prev_port, allow_type_mismatch=True)
    prev_port = ref.ports["e2"]

    ref = c << padding_height_compass
    ref.connect("e1", prev_port, allow_type_mismatch=True)
    prev_port = ref.ports["e3"]

    turn_ports_naming = [("e2", "e1"), ("e1", "e2")]

    for i in range(num_turns):
        turn_connect_name, turn_prev_name = turn_ports_naming[i % 2]
        prev_port = _optimal_full_turn_with_spacing(
            c, turn, spacing_compass, turn_connect_name, turn_prev_name, prev_port
        )
        vertical_compass = padding_height_compass if i == num_turns - 1 else height_compass
        ref = c << vertical_compass
        ref.connect("e1", prev_port, allow_type_mismatch=True)
        prev_port = ref.ports["e3"]

    ref = c << turn
    turn_connect_name, turn_prev_name = turn_ports_naming[num_turns % 2]
    ref.connect(turn_connect_name, prev_port, allow_type_mismatch=True)
    prev_port = ref.ports[turn_prev_name]

    end_wg = c << padding_compass
    end_wg.connect("e1", prev_port, allow_type_mismatch=True)

    c.add_port("e1", start_wg.ports["e1"])
    c.add_port("e2", end_wg.ports["e3"])
    return c


def _optimal_full_turn_with_spacing(
    component, optimal_turn, spacing_compass, turn_connect_name, turn_prev_name, prev_port
):
    """
    Helper function to create a full turn with spacing in the meander pattern.

    Args:
        component: The parent component.
        optimal_turn: The optimal 90-degree turn component.
        spacing_compass: The spacing component.
        turn_connect_name (str): Port name for connecting the turn.
        turn_prev_name (str): Port name for the previous turn.
        prev_port: The previous port reference.

    Returns:
        The new previous port after adding the turn and spacing.
    """
    c = component
    ref = c << optimal_turn
    ref.connect(turn_connect_name, prev_port, allow_type_mismatch=True)
    prev_port = ref.ports[turn_prev_name]

    ref = c << spacing_compass
    ref.connect("e1", prev_port, allow_type_mismatch=True)
    prev_port = ref.ports["e3"]

    ref = c << optimal_turn
    ref.connect(turn_connect_name, prev_port, allow_type_mismatch=True)
    prev_port = ref.ports[turn_prev_name]
    return prev_port
