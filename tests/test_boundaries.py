from boundary_conditions import Boundary
from mesh import Mesh
from domain import Domain
import pytest

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
    return b

def test_boundary_class_initialization(boundary):
    b = boundary
    assert b.conditions['left'] == {}
    assert b.conditions['right'] == {}
    assert b.conditions['top'] == {}
    assert b.conditions['bottom'] == {}

def test_boundary_integrates_with_mesh_class_correctly(boundary):
    b = boundary
    assert b.mesh.nx == 4
    assert b.mesh.ny == 4
    assert len(b.mesh.p_nodes) == 4
    assert len(b.mesh.u_nodes) == 4
    assert len(b.mesh.v_nodes) == 5

def test_apply_pressure_boundary_is_correct(boundary):
    b = boundary
    b.mesh.p_nodes[0][3].p_old = 3
    b.apply_pressure_boundary('right', 0)
    assert b.mesh.p_nodes[0][3].p_old == 0
    assert b.mesh.p_nodes[1][3].p_old == 0
    assert b.mesh.p_nodes[2][3].p_old == 0
    assert b.mesh.p_nodes[3][3].p_old == 0

def test_apply_velocity_boundary_is_correct(boundary):
    b = boundary
    b.mesh.u_nodes[0][0].u_old = 4
    b.mesh.v_nodes[0][2].v = 5
    b.apply_velocity_boundary('left', u_value=.001)
    b.apply_velocity_boundary('top', v_value=0)
    b.apply_velocity_boundary('bottom', v_value=0)
    assert b.mesh.u_nodes[0][0].u_old == .001
    assert b.mesh.u_nodes[0][0].u == .001
    assert b.mesh.u_nodes[1][0].u == .001
    assert b.mesh.v_nodes[0][0].v == 0
    assert b.mesh.v_nodes[0][1].v == 0
    assert b.mesh.v_nodes[0][2].v == 0
    assert b.mesh.v_nodes[4][0].v == 0
    assert b.mesh.v_nodes[4][1].v == 0

