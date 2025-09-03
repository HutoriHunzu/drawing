# BaseArmConfig
```python
    CONNECTION_PORT_NAME: str = Field("connection", exclude=True)
    GAP_PORT_NAME: str = Field("gap", exclude=True)
```

Base configuration for a junctions' arm component.

### Attributes:
*  layer (LayerSpec): Layer specification for the arm component.

### Constants:
* CONNECTION_PORT_NAME (str):
* GAP_PORT_NAME (str):

### Methods:
```python
def build(self) -> gf.Component
```
Abstract method

```python
def total_length(self) -> float
```
Abstract method

## RegularArmConfig
```python
    length: float = 10.0
    width: float = 1.0
```

Configuration for a rectangular arm component.

### Attributes:
*  length (float): Length of the arm.
*  width (float): Width of the arm.
*  layer (LayerSpec): Layer specification for the arm component.

### Constants:
* CONNECTION_PORT_NAME (str):
* GAP_PORT_NAME (str):

### Methods:
```python
def build(self) -> gf.Component
```
Creates a rectangular arm component.
The function uses @gf.cell, then the component is cached and named. 

```python
def total_length(self) -> float
```
Returns the total length of the arm.

## FunnelrArmConfig
```python
    wide_length: float = 10.0
    wide_width: float = 5.0
    narrow_length: float = 10.0
    narrow_width: float = 2.0
```

Configuration for a funnel arm component.

### Attributes:
*  wide_length (float): Length of the wide part of the funnel.
*  wide_width (float): Width of the wide part of the funnel.
*  narrow_length (float): Length of the narrow part of the funnel.
*  narrow_width (float): Width of the narrow part of the funnel.
*  layer (LayerSpec): Layer specification for the arm component.

### Constants:
* CONNECTION_PORT_NAME (str):
* GAP_PORT_NAME (str):

### Methods:
```python
def build(self) -> gf.Component
```
Creates a funnel arm component.
The function uses @gf.cell, then the component is cached and named. 

```python
def total_length(self) -> float
```
Returns the total length of the arm.

## TArmConfig
```python
    wide_length: float = 10.0
    wide_width: float = 5.0
    narrow_length: float = 10.0
    narrow_width: float = 2.0
```

Configuration for a T arm component.

### Attributes:
*  horizontal_length (float): Length of the horizontal section of the T-arm.
*  horizontal_width (float): Width of the horizontal section of the T-arm.
*  vertical_length (float): Length of the vertical section of the T-arm.
*  vertical_width (float): Width of the vertical section of the T-arm.
*  layer (LayerSpec): Layer specification for the arm component.

### Constants:
* CONNECTION_PORT_NAME (str):
* GAP_PORT_NAME (str):

### Methods:
```python
def build(self) -> gf.Component
```
Creates a T arm component.
The function uses @gf.cell, then the component is cached and named. 

```python
def total_length(self) -> float
```
Returns the total length of the arm.


# BaseJunctionConfig
```python
    gap_length: float = 1.0
    gap_layer: gf.typings.LayerSpec = (1,11)
    gap_create: bool = True

    junction_type: junctionTypeEnum = "DOLAN"

    LEFT_PREFIX: str = Field("left_", exclude=True)
    RIGHT_PREFIX: str = Field("right_", exclude=True)
```

Base configuration for a junctions' arm component.

### Attributes:
*  gap_length (float): Length of the gap.
*  gap_layer (LayerSpec): Layer specification for the gap.
*  gap_create (bool): Whether to create a gap in the junction.
*  junction_type (junctionTypeEnum): The type of junction
*  layer (LayerSpec): Layer specification for the arm component.

### Constants:
* LEFT_PREFIX (str):
* RIGHT_PREFIX (str):

### Methods:
```python
def build(self) -> gf.Component
```
Abstract method

```python
def total_length(self) -> float
```
Abstract method

```python
def get_left_arm_config(self) -> BaseArmConfig
```
Abstract method

```python
def get_right_arm_config(self) -> BaseArmConfig
```
Abstract method

## SymmetricJunctionConfig
```python
    arm: BaseArmConfig = RegularArmConfig()
```

Configuration for symmetric junction component.

### Attributes:
*  arm (BaseArmConfig): Configuration for the arm component.
*  gap_length (float): Length of the gap.
*  gap_layer (LayerSpec): Layer specification for the gap.
*  gap_create (bool): Whether to create a gap in the junction.
*  junction_type (junctionTypeEnum): The type of junction
*  layer (LayerSpec): Layer specification for the arm component.

### Constants:
* LEFT_PREFIX (str):
* RIGHT_PREFIX (str):
* LEFT_CONNECTING_PORT_NAME (str):
* RIGHT_CONNECTING_PORT_NAME (str):

### Methods:
```python
def build(self) -> gf.Component
```
Creates a symmetric junction component.
The function uses @gf.cell, then the component is cached and named. 

```python
def total_length(self) -> float
```
Returns the total length of the junction.

```python
def get_left_arm_config(self) -> BaseArmConfig
```
Return the armConfig of the left arm

```python
def get_right_arm_config(self) -> BaseArmConfig
```
Return the armConfig of the right arm

## AntisymmetricJunctionConfig
```python
    arm: BaseArmConfig = RegularArmConfig()
```

Configuration for antisymmetric junction component.

### Attributes:
*  arm (BaseArmConfig): Configuration for the arm component.
*  gap_length (float): Length of the gap.
*  gap_layer (LayerSpec): Layer specification for the gap.
*  gap_create (bool): Whether to create a gap in the junction.
*  junction_type (junctionTypeEnum): The type of junction
*  layer (LayerSpec): Layer specification for the arm component.

### Constants:
* LEFT_PREFIX (str):
* RIGHT_PREFIX (str):
* LEFT_CONNECTING_PORT_NAME (str):
* RIGHT_CONNECTING_PORT_NAME (str):

### Methods:
```python
def build(self) -> gf.Component
```
Creates a symmetric junction component.
The function uses @gf.cell, then the component is cached and named. 

```python
def total_length(self) -> float
```
Returns the total length of the junction.

```python
def get_left_arm_config(self) -> BaseArmConfig
```
Return the armConfig of the left arm

```python
def get_right_arm_config(self) -> BaseArmConfig
```
Return the armConfig of the right arm