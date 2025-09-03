### SquidConfig
```python
    flux_hole_length: float = 15
    flux_hole_width: float = 5
    outer_length: float = 20
    outer_width: float = 10
    junction_gap_length: float = 2
    layer: LayerSpec = DEFAULT_LAYER
    bridges_layer: LayerSpec | None = None
```

Configuration for a squid component.

Attributes:
*  flux_hole_width (float): Width of the flux hole.
*  flux_hole_length (float): Length of the flux hole.
*  outer_length (float): Length of the outer rectangle.
*  outer_width (float): Width of the outer rectangle.
*  junction_gap_length (float): Length of the gap between junctions.
*  layer (LayerSpec): Layer specification for the squid component.
*  bridges_layer (LayerSpec | None): Optional layer specification for the bridges over the gap.