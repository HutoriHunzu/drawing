# Transmon Layout Library

This repository provides a Python library for designing custom transmon layouts using [gdsfactory](https://github.com/gdsfactory/gdsfactory). The library integrates several configurable components—such as pads, tapers, junctions, and an optional antenna—into a unified layout via the `TransmonConfig` class.

## Overview

The `TransmonConfig` class encapsulates all the parameters required to build a transmon layout. It manages the integration of sub-components, including:
- **Pads**: For electrical connections.
- **Tapers**: To transition between different geometries.
- **Junctions**: For connecting tapers to pads.
- **Antenna (Optional)**: For additional functionality.

This configuration simplifies complex layout creation by automatically handling port connections, merging of shapes, and corner smoothing.

## Installation
   ```bash
   git clone https://github.com/HutoriHunzu/drawing.git
   pip install -e drawing
```

## Usage
This module is specified for the creation of transmons and exporting them to HFSS using
pyaedt. An example for creating a transmon:
```python

import matplotlib.pyplot as plt
from drawing import TransmonConfig
# Build the transmon layout
tr = TransmonConfig().build()

# Optionally, print port information (uncomment if needed)
# tr.pprint_ports()

# Visualize the ports on the component
tr.draw_ports()

# Write the layout to a GDS file (without metadata)
tr.write_gds('gds_files/testing.gds', with_metadata=False)

# Plot the layout and show the figure
tr.plot()
plt.show()
```
One could also modify the configuration by adding different values for the attributes
for example:

```python

import matplotlib.pyplot as plt
from drawing import TransmonConfig, IntegrationConfig
# Build the transmon layout
integration_config = IntegrationConfig(use_antenna=False)
tr = TransmonConfig(integration_config=integration_config).build()

# Visualize the ports on the component
tr.draw_ports()

# Write the layout to a GDS file (without metadata)
tr.write_gds('gds_files/testing.gds', with_metadata=False)

# Plot the layout and show the figure
tr.plot()
plt.show()
```
Now there won't be antenna in the transmon.


# Documentation
## Classes

### TransmonConfig
```python
class TransmonConfig(BaseModel):
    integration_config: IntegrationConfig = IntegrationConfig()
    pad: PadConfig = PadConfig()
    taper: TaperConfig = TaperConfig()
    junction: SupportedJunctions = RegularJunction()
    antenna: AntennaConfig = AntennaConfig()
    layer: LayerSpec = DEFAULT_LAYER
```
Configuration for constructing a complete transmon layout using GDSFactory.

This configuration encapsulates parameters for integrating pads, tapers, junctions,
and an optional antenna. It manages shape merging, smoothing of corners, and the overall
connectivity required to build a transmon component.

Attributes:
* integration_config (IntegrationConfig): Settings controlling integration features such as feature radius and antenna usage.
* pad (PadConfig): Configuration parameters for pad dimensions and layout.
* taper (TaperConfig): Configuration for taper shapes.
* junction (SupportedJunctions): Junction configuration that connects tapers to pads. Defaults to a regular junction.
* antenna (AntennaConfig): Configuration for the optional antenna shape.
* layer (LayerSpec): GDS layer specification applied to all components.

### IntegrationConfig
```python
class IntegrationConfig(BaseModel):
    feature_radius: float = 10.0
    use_antenna: bool = True
```
Configuration for integration features.

Attributes:
* feature_radius (float): Feature radius.
* use_antenna (bool): Flag to use antenna or not.

### AntennaConfig
```python
class AntennaConfig(BaseModel):
    length: float = 1400
    width: float = 100
    radius: float = 250
    layer: LayerSpec = DEFAULT_LAYER
```

Configuration for building an antenna component in a transmon layout.

This configuration defines the dimensions and layer for the antenna. The antenna
consists of a rectangular (compass) part and a circular part, which are connected
to form the final shape.

Attributes:
* length (float): Length of the rectangular part.
* width (float): Width of the rectangular part.
* radius (float): Radius of the circular part.
* layer (LayerSpec): GDS layer specification for the antenna.

### PadConfig
```python
class PadConfig(BaseModel):
    width: float = 400
    height: float = 1000
    radius: float = 100
    distance: float = 150
    layer: LayerSpec = DEFAULT_LAYER
```
Configuration for pad components used in the transmon layout.

Defines the size, corner radius, spacing, and layer for the pads. Also handles
port placement for electrical connectivity.

Attributes:
* width (float): Pad width.
* height (float): Pad height.
* radius (float): Corner radius for smoothing (0 for sharp edges).
* distance (float): Horizontal separation between pads.
* layer (LayerSpec): GDS layer specification.

### TaperConfig
```python
class TaperConfig(BaseModel):
    length: float = 65
    wide_width: float = 45
    narrow_width: float = 1
    extra_length: float = 5
    layer: LayerSpec = DEFAULT_LAYER
```
Configuration for taper components used to transition between different widths.

This configuration defines the dimensions of a taper as well as the additional
extra length for connection components.

Attributes:
* length (float): Length of the taper.
* wide_width (float): Starting width of the taper.
* narrow_width (float): Ending width of the taper.
* extra_length (float): Additional length for the connection (compass).
* layer (LayerSpec): GDS layer specification.

### RegularJunction
```python
class BaseJunction(BaseModel):
    layer: LayerSpec = DEFAULT_LAYER
    junction_focus_layer: LayerSpec = JUNCTION_FOCUS_LAYER
```
Virtual Class for creating junction classes between tapers in a transmon layout.

Attributes:
* layer (LayerSpec): GDS layer specification.

### RegularJunction
```python
class RegularJunction(BaseModel):
    type: Literal['regular'] = 'regular'
    width: float = 1
    gap: float = 3
    length: float = 10
    layer: LayerSpec = DEFAULT_LAYER
    junction_focus_layer: LayerSpec = JUNCTION_FOCUS_LAYER
```
Configuration for creating a regular junction between tapers in a transmon layout.

Attributes:
* type (Literal['regular']): Fixed type for a regular junction.
   Literal['regular'] only allowed the value 'regular'. Hence type is a constant.
* width (float): Junction width.
* gap (float): Gap between the connected tapers.
* length (float): Nominal length for the junction.
* layer (LayerSpec): GDS layer specification.

### IrregularJunction
```python
class IrregularJunction(BaseModel):
    type: Literal['irregular'] = 'irregular'
    width: float = 1
    thickness: float = 2
    vertical_length: float = 6
    gap: float = 3
    layer: LayerSpec = DEFAULT_LAYER
    junction_focus_layer: LayerSpec = JUNCTION_FOCUS_LAYER
```

Configuration for creating an irregular junction between tapers in a transmon layout.

Attributes:
*  type (Literal['irregular']): Fixed type for the irregular junction.
   Literal['irregular'] only allowed the value 'irregular'. Hence type is a constant. 
*  width (float): Width of the junction.
*  thickness (float): Thickness parameter for the asymmetric elbow shape.
*  vertical_length (float): Vertical length for the elbow shape.
*  gap (float): Gap between junction components.
*  layer (LayerSpec): GDS layer specification.

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
  
  
## Types

### Layer
```python
Layer: TypeAlias = tuple[int, int]
LayerSpec: TypeAlias = Layer | str | int | LayerEnum

DEFAULT_LAYER = (1, 0)
JUNCTION_FOCUS_LAYER = (33, 0)
```
