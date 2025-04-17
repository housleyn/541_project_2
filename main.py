import numpy as np
import matplotlib.pyplot as plt
from domain import Domain
from mesh import Mesh
from boundary_conditions import Boundary
from material import Material
from SIMPLE import SIMPLE
from plotting import (
    extract_pressure_grid, plot_filled_contour, plot_pressure_centerline, plot_convergence,
    extract_u_velocity_grid, extract_v_velocity_grid, plot_mass_flow_convergence, 
)

d = Domain()
d.define_lower_boundary(lambda x, y: 0)
d.define_upper_boundary(lambda x, y: .01)
d.define_left_boundary(lambda y, x=None: 0)
d.define_right_boundary(lambda y, x=None: .05)

mesh = Mesh(d, 40, 40)
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

simulation = SIMPLE(mesh, b, m)
simulation.alphau = simulation.alphav = simulation.alpha_p = 0.5

simulation.max_iterations = 50
simulation.run()

X, Y, P = extract_pressure_grid(mesh)
plot_filled_contour(X, Y, P, title="Pressure Field")

Xu, Yu, U = extract_u_velocity_grid(mesh)
plot_filled_contour(Xu, Yu, U, title="U Velocity Field")

Xv, Yv, V = extract_v_velocity_grid(mesh)
plot_filled_contour(Xv, Yv, V, title="V Velocity Field")

plot_pressure_centerline(mesh)
plot_mass_flow_convergence(mesh, m.rho)