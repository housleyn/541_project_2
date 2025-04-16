import numpy as np
import matplotlib.pyplot as plt
from domain import Domain
from mesh import Mesh
from boundary_conditions import Boundary
from material import Material
from SIMPLE import SIMPLE

d = Domain()
d.define_lower_boundary(lambda x, y: 0)
d.define_upper_boundary(lambda x, y: .01)
d.define_left_boundary(lambda y, x=None: 0)
d.define_right_boundary(lambda y, x=None: .05)

mesh = Mesh(d, 4, 4)
mesh.construct_mesh()

b = Boundary(mesh)
b.apply_pressure_boundary('right', 0)
b.apply_velocity_boundary('left', u_value=.001)
b.apply_velocity_boundary('left', v_value=0)
b.apply_velocity_boundary('top', v_value=0)
b.apply_velocity_boundary('bottom', v_value=0)

m = Material()
m.rho = 1000
m.mu = .001

mesh.plot_nodes_with_indices()