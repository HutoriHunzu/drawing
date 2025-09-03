## SnailConfig
```python
    flux_hole_width: float = 5
    flux_hole_length: float = 10

    flux_hole_bar_length: float = 5

    top_left_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    top_middle_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    top_right_junction: BaseJunctionConfig = SymmetricJunctionConfig()
    bottom_junction: BaseJunctionConfig = SymmetricJunctionConfig(
        arm = RegularArmConfig(
            length = ( SymmetricJunctionConfig().total_length() * 3 - 1 ) / 2
        )
    )
```

Configuration for a Snail component.

### Attributes:
*  flux_hole_width (float): Width of the flux hole.
*  flux_hole_length (float): Length of the flux hole.
*  outer_length (float): Length of the outer rectangle.
*  outer_width (float): Width of the outer rectangle.
*  junction_gap_length (float): Length of the gap between junctions.
*  layer (LayerSpec): Layer specification for the squid component.
*  bridges_layer (LayerSpec | None): Optional layer specification for the bridges over the gap.
  
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

```python
def bottom_junction_length_arm_length(self) -> float
```
Calculates the length of the bottom junction arm based on the current configuration of top junctions.