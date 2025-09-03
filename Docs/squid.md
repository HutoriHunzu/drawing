## SquidConfig
```python
class SquidConfig(BaseConfig):
    flux_hole_width: float = 5
    flux_hole_length: float = 10

    flux_hole_bar_length: float = 5

    top_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    bottom_junction: BaseJunctionConfig = SymmetricJunctionConfig()

    layer: LayerSpec = DEFAULT_LAYER

    LEFT_CONNECTING_PORT_NAME: str = "left_connection"
    RIGHT_CONNECTING_PORT_NAME: str = "right_connection"
```

Configuration for a squid component.

### Attributes:
*  flux_hole_width (float): Width of the flux hole.
*  flux_hole_length (float): Length of the flux hole.
*  flux_hole_bar_length (float): Length of the flux hole bar.
*  top_junction (BaseJunctionConfig): Configuration for the top junction.
*  bottom_junction (BaseJunctionConfig): Configuration for the bottom junction.
*  layer (LayerSpec): Layer specification for the squid component.

### Constants:
* LEFT_CONNECTING_PORT_NAME (str):
* RIGHT_CONNECTING_PORT_NAME (str):

### Methods:
```python
def build(self) -> gf.Component
```
Creates a Squid component.
The function uses @gf.cell, then the component is cached and named. 

```python
def get_jopherson_junctions(self) -> list[BaseJunctionConfig]
```
Returns a list of the junctions
