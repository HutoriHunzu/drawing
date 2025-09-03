"""
Shared utility functions for GDS component creation and manipulation.

This module contains functions for merging shapes, smoothing corners, and
a decorator to automatically merge referenced shapes in a component.
"""

import gdsfactory as gf
from gdsfactory.typings import LayerSpec
from typing import Tuple
from functools import wraps

# Type aliases
Coordinate = Tuple[float, float]
Size = Tuple[float, float]

DEFAULT_LAYER = (1, 0)
DEFAULT_WAFER_LAYER = (60, 0)
JUNCTION_FOCUS_LAYER = (33, 0)
JUNCTION_PICTURE_LAYER = (50, 0)
SAMPLE_AREA_INDICATOR_LAYER = (40, 0)
DEFAULT_NUM_POINTS = 300

ONE_INCH_IN_MICROMETER = 25400


@gf.cell
def merge_referenced_shapes(
    component: gf.Component,
        layer: LayerSpec = DEFAULT_LAYER
) -> gf.Component:
    """
    Merges all referenced shapes in a component into a single component.

    This function processes the component's merged polygons and ports, returning
    a new component that contains the unified geometry.

    Args:
        component (gf.Component): The component with shape references.
        layer (LayerSpec): Target GDS layer for merged shapes.

    Returns:
        gf.Component: A component with merged geometries.
    """
    merged_component = gf.Component()
    for lyr, polygons in component.get_polygons(merge=True).items():
        for polygon in polygons:
            merged_component.add_polygon(polygon, layer=lyr)
    merged_component.add_ports(component.ports)
    return merged_component


@gf.cell
def smooth_corners(
    component: gf.Component,
    radius: float = 1.0,
    num_points: int = DEFAULT_NUM_POINTS,
    layer: LayerSpec = DEFAULT_LAYER,
) -> gf.Component:
    """
    Smooths all corners in a component with a given radius.

    Args:
        component (gf.Component): The component whose corners will be smoothed.
        radius (float): Rounding radius in microns.
        num_points (int): Points per full circle for rounding.
        layer (LayerSpec): GDS layer for the smoothed component.

    Returns:
        gf.Component: A new component with rounded corners.
    """
    c = gf.Component()
    radius_db = int(round(radius * 1000))
    for _, polygons in component.get_polygons().items():
        for polygon in polygons:
            p_round = polygon.round_corners(radius_db, radius_db, num_points)
            c.add_polygon(p_round, layer=layer)
    c.add_ports(component.ports)
    return c


def merge_decorator(func):
    """
    Decorator that merges referenced shapes after the decorated function returns a component.

    Args:
        func: The function that builds a component.

    Returns:
        The merged component.
    """
    @wraps(func)
    def foo(*args, **kwargs):
        c = func(*args, **kwargs)
        return merge_referenced_shapes(c)
    return foo

@gf.cell
def array_mirror_x(
    component: gf.Component,
    mirror_distance: float = 0,
    rows: int = 1,
    column_pitch: float = 200,
    row_pitch: float = 200,
) -> gf.Component:
    """
    Args:
        cols: number of columns.
        rows: number of rows.
        column_pitch: distance between columns.
        row_pitch: distance between rows.
        pad: pad cell.
    """
    m = gf.Component()
    component_ref = m << component
    copy_ref = m << component.copy().mirror_x()

    copy_ref.movex((component_ref.xmax - copy_ref.xmin) + mirror_distance)

    c = gf.Component()
    c.add_ref(
        m, columns=1, rows=rows, column_pitch=(column_pitch + copy_ref.xsize), row_pitch=(row_pitch + copy_ref.ysize)
    )
    return c

@gf.cell
def array_mirror_y(
    component: gf.Component,
    mirror_distance: float = 0,
    cols: int = 1,
    column_pitch: float = 200,
    row_pitch: float = 200,
) -> gf.Component:
    """
    Args:
        cols: number of columns.
        rows: number of rows.
        column_pitch: distance between columns.
        row_pitch: distance between rows.
        pad: pad cell.
    """
    m = gf.Component()
    component_ref = m << component
    copy_ref = m << component.copy().mirror_y()

    copy_ref.movey((component_ref.ymax - copy_ref.ymin) + mirror_distance)

    c = gf.Component()
    c.add_ref(
        m, columns=cols, rows=1, column_pitch=(column_pitch + copy_ref.ysize), row_pitch=(row_pitch + copy_ref.xsize)
    )
    return c