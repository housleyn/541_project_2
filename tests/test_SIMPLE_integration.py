from SIMPLE import SIMPLE
from node import Node
from control_surfaces import ControlSurface
from mesh import Mesh
from domain import Domain
from boundary_conditions import Boundary
from material import Material
import pytest 
import numpy as np


@pytest.fixture
def domain():
    d = Domain()
    d.define_lower_boundary(lambda x, y: 0)
    d.define_upper_boundary(lambda x, y: .01)
    d.define_left_boundary(lambda y, x=None: 0)
    d.define_right_boundary(lambda y, x=None: .05)
    return d

@pytest.fixture
def mesh(domain):
    mesh = Mesh(domain, 4, 4)
    mesh.construct_mesh()
    return mesh

@pytest.fixture
def boundary(mesh):
    b = Boundary(mesh)
    b.apply_pressure_boundary('right', 0)
    b.apply_velocity_boundary('left', u_value=.001)
    b.apply_velocity_boundary('left', v_value=0)
    b.apply_velocity_boundary('top', v_value=0)
    b.apply_velocity_boundary('bottom', v_value=0)
    return b

@pytest.fixture
def material():
    m = Material()
    m.rho = 1000
    m.mu = .001
    return m

@pytest.fixture
def simple(mesh, boundary, material):
    return SIMPLE(mesh, boundary, material)
@pytest.fixture
def first_iteration_interior(simple):
    simple.generate_initial_guesses()
    cs = simple.mesh.u_nodes[1][1]
    mu = simple.mu  
    rho = simple.rho
    dx = simple.mesh.dx
    dy = simple.mesh.dy
    alphau = 0.5
    pe = simple.mesh.p_nodes[1][1].p_old
    pw = simple.mesh.p_nodes[1][0].p_old
    uE_old = simple.mesh.u_nodes[1][2].u_old
    uW_old = simple.mesh.u_nodes[1][0].u_old
    vUL_old = simple.mesh.v_nodes[2][1].v_old
    vUR_old = simple.mesh.v_nodes[2][2].v_old
    vBL_old = simple.mesh.v_nodes[1][1].v_old
    vBR_old = simple.mesh.v_nodes[1][2].v_old
    j = 1
    ny = simple.mesh.ny
    cs.calculate_x_coefficients(mu, rho, dx, dy, alphau, pe, pw,
                                 uE_old, uW_old, vUL_old, vUR_old, vBL_old, vBR_old,j, ny)
    return cs



@pytest.fixture
def first_iteration_interior_y(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    cs = simple.mesh.v_nodes[1][2]
    mu = simple.mu
    rho = simple.rho
    dx = simple.mesh.dx
    dy = simple.mesh.dy
    alphav = 0.5
    ps = simple.mesh.p_nodes[0][1].p_old
    pn = simple.mesh.p_nodes[1][1].p_old
    vN_old = simple.mesh.v_nodes[2][2].v_old
    vS_old = simple.mesh.v_nodes[0][2].v_old
    uUL = simple.mesh.u_nodes[1][1].u
    uUR = simple.mesh.u_nodes[1][2].u
    uBL = simple.mesh.u_nodes[0][1].u
    uBR = simple.mesh.u_nodes[0][2].u
    cs.calculate_y_coefficients(mu, rho, dx, dy, alphav, ps, pn,
                                 vN_old, vS_old, uUL, uUR, uBL, uBR)
    return cs 

def test_control_surface_calculation_interior(first_iteration_interior):
    cs = first_iteration_interior
    assert cs.aE == pytest.approx(.0002)
    assert cs.aW == pytest.approx(.0027)
    assert cs.aN == pytest.approx(.005)
    assert cs.aS == pytest.approx(.00625)
    assert cs.aP == pytest.approx(0.0283)
    assert cs.b == pytest.approx(1.415e-5)

def test_control_surface_calculation_interior_x(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    cs = simple.mesh.u_nodes[1][1]
    assert cs.aE == pytest.approx(.0002)
    assert cs.aW == pytest.approx(.0027)
    assert cs.aN == pytest.approx(.005)
    assert cs.aS == pytest.approx(.00625)
    assert cs.aP == pytest.approx(0.0283)
    assert cs.b == pytest.approx(1.415e-5)


def test_control_surface_calculation_inlet(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    cs = simple.mesh.u_nodes[0][0]
    assert cs.aE == 0
    assert cs.aW == 0
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1 
    assert cs.b == 0.001
def test_control_surface_calculation_outlet(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    cs = simple.mesh.u_nodes[1][4]
    assert cs.aE == 0
    assert cs.aW == 1
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1 
    assert cs.b == 0.0

def test_control_surface_calculation_top_wall(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    cs = simple.mesh.u_nodes[3][1]
    mu = simple.mu
    dx = simple.mesh.dx
    dy = simple.mesh.dy
    assert cs.aE == pytest.approx(.0002)
    assert cs.aW == pytest.approx(.0027)
    assert cs.aN == pytest.approx(.005)
    # assert cs.aS == 0
    assert cs.aP == pytest.approx(0.0383)
    assert cs.b == pytest.approx(1.915e-5)

def test_control_surface_calculation_bottom_wall(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    cs = simple.mesh.u_nodes[0][1]
    mu = simple.mu
    dx = simple.mesh.dx
    dy = simple.mesh.dy
    assert cs.aE == pytest.approx(.0002)
    assert cs.aW == pytest.approx(.0027)
    # assert cs.aN == 0
    assert cs.aS == pytest.approx(.00625)
    assert cs.aP == pytest.approx(0.0358)
    assert cs.b == pytest.approx(1.79e-5)

def test_control_surface_calculation_corners(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    cs = simple.mesh.u_nodes[0][0]
    assert cs.aE == 0
    assert cs.aW == 0
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1 
    assert cs.b == 0.001
    
    cs = simple.mesh.u_nodes[3][0]
    assert cs.aE == 0
    assert cs.aW == 0
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1
    assert cs.b == 0.001

    cs = simple.mesh.u_nodes[0][4]
    assert cs.aE == 0
    assert cs.aW == 1
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1
    assert cs.b == 0.0

    cs = simple.mesh.u_nodes[3][4]
    assert cs.aE == 0
    assert cs.aW == 1
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1 
    assert cs.b == 0.0

def test_v_inlet(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    simple.calculate_v_field()
    cs = simple.mesh.v_nodes[1][0]
    assert cs.aE == 0
    assert cs.aW == 0
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1 
    assert cs.b == 0

def test_v_outlet(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    simple.calculate_v_field()
    cs = simple.mesh.v_nodes[1][5]
    assert cs.aE == 0
    assert cs.aW == 0
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1 
    assert cs.b == 0.0

def test_v_interior(first_iteration_interior_y):
    cs = first_iteration_interior_y
    assert cs.aE == pytest.approx(.0002)
    assert cs.aW.item() == pytest.approx(.0022393, abs=1e-4)
    assert cs.aN == pytest.approx(.005)
    assert cs.aS == pytest.approx(.005625)
    assert cs.aP.item() == pytest.approx(0.027281, abs=1e-4)
    assert cs.b.item() == pytest.approx(1.364e-6, abs=1e-4)

def test_v_top_wall(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    simple.calculate_v_field()
    cs = simple.mesh.v_nodes[4][1]
    assert cs.aE == 0
    assert cs.aW == 0
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1
    assert cs.b == 0

def test_v_bottom_wall(simple):
    simple.generate_initial_guesses()
    simple.calculate_u_field()
    simple.calculate_v_field()
    cs = simple.mesh.v_nodes[0][1]
    assert cs.aE == 0
    assert cs.aW == 0
    assert cs.aN == 0
    assert cs.aS == 0
    assert cs.aP == 1 
    assert cs.b == 0.0