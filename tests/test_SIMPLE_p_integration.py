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
    s = SIMPLE(mesh, boundary, material)
    s.generate_initial_guesses()
    s.calculate_u_field()
    s.calculate_v_field()
    s.calculate_p_prime_field()
    return s
def test_p_interior_inputs(simple):
    s = simple
    v = s.mesh.v_nodes
    u = s.mesh.u_nodes
    assert u[1][2].aP * s.alphau == pytest.approx(.01415)

def test_p_interior(simple):
    s = simple 
    p = s.mesh.p_nodes[1][1]
    assert p.aE == pytest.approx(.22084, rel=1e-2)
    assert p.aW == pytest.approx(.22084, rel=1e-2)
    assert p.aN.item() == pytest.approx(5.6058632)
    assert p.aS.item() == pytest.approx(5.7274711)
    assert p.aP.item() == pytest.approx(11.7750305)
    assert p.b.item() == pytest.approx(-0.0001597, rel=1e-2)

def test_p_near_wall(simple):
    s = simple 
    p = s.mesh.p_nodes[0][1]
    assert p.aE == pytest.approx(.17458, rel=1e-2)
    assert p.aW == pytest.approx(.17458, rel=1e-2)
    assert p.aN == pytest.approx(5.7274711, rel=1e-2)
    assert p.aS == pytest.approx(.078125, rel=1e-2)
    assert p.aP == pytest.approx(6.1547552, rel=1e-2)

def test_p_prime_values(simple):
    s = simple 
    p = s.mesh.p_nodes[0][0]
    assert p.p_prime.item() == pytest.approx(.00344, rel=1e-2)

def test_p_new(simple):
    s = simple
    s.calculate_p_field()
    p = s.mesh.p_nodes[0][0]
    assert p.p.item() == pytest.approx(.00444, rel=1e-2)
def test_p_new_2(simple):
    s = simple
    s.calculate_p_field()
    p = s.mesh.p_nodes[1][1]
    assert p.p.item() == pytest.approx(.003147, rel=1e-2)

def test_p_new_3(simple):
    s = simple
    s.calculate_p_field()
    p = s.mesh.p_nodes[1][0]
    assert p.p.item() == pytest.approx(.004559, rel=1e-2)
def test_p_prime(simple):
    s = simple
    p = s.mesh.p_nodes[3][0]
    assert p.p_prime.item() == pytest.approx(.00389, rel=1e-2)

def test_p_prime_2(simple):
    s = simple
    p = s.mesh.p_nodes[2][0]
    assert p.p_prime.item() == pytest.approx(.00372, rel=1e-2)




def test_p_new_4(simple):
    s = simple
    s.calculate_p_field()
    p = s.mesh.p_nodes[3][0]
    assert p.p.item() == pytest.approx(.00489, rel=1e-2)

def test_p_new_5(simple):
    s = simple
    s.calculate_p_field()
    p = s.mesh.p_nodes[3][1]
    assert p.p == pytest.approx(.00348, rel=1e-2)

def test_p_new_6(simple):
    s = simple
    s.calculate_p_field()
    p = s.mesh.p_nodes[2][3]
    assert p.p.item() == pytest.approx(.001, rel=1e-2)

def test_u_new(simple):
    s = simple
    s.calculate_p_field()
    s.calculate_new_u_field()
    u = s.mesh.u_nodes[0][0]
    assert u.u.item() == pytest.approx(.001, rel=1e-2)
    