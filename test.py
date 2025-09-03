from drawing import *
from drawing.junction.antisymmetric_junction import AntisymmetricJunctionConfig
from drawing.junction.symmetric_junction import SymmetricJunctionConfig
from drawing.junction.funnel_arm import FunnelrArmConfig
import matplotlib.pyplot as plt
import gdsfactory as gf
from drawing.snail.snail import SnailConfig
plotc = gf.Component()

s = SnailConfig()
s_ref = plotc << s.build()
plotc.add_ports(s_ref.ports, prefix="Snail")
plotc.draw_ports()
plotc.pprint_ports()
plotc.plot()

print(SymmetricJunctionConfig().total_length())

# print(SymmetricJunctionConfig(arm=FunnelrArmConfig()).total_length())
# print(SymmetricJunctionConfig().total_length())

plt.show()