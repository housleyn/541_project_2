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

def test_simple_initialization(simple):
    assert simple.mesh is not None
    assert simple.boundary is not None
    assert simple.rho == 1000
    assert simple.mu == .001

def test_simple_integrates_with_other_classes(simple):
    assert isinstance(simple.mesh, Mesh)
    assert isinstance(simple.boundary, Boundary)
    assert isinstance(simple.mesh.p_nodes[0][0], Node)
    assert isinstance(simple.mesh.u_nodes[0][0], ControlSurface)

def test_simple_generate_initial_guesses_u_field_is_correct_and_didnt_change_boundaries(simple):
    simple.generate_initial_guesses_u_field()
    ny = simple.mesh.ny
    nx = simple.mesh.nx + 1  # u_nodes has nx+1 columns

    for j in range(ny):
        for i in range(nx):
            u = simple.mesh.u_nodes[j][i].u_old
            assert u == 0.001, f"u[{j}][{i}] = {u}, expected 0.001"


def test_simple_generate_initial_guesses_v_field_is_correct_and_didnt_change_boundaries(simple):
    simple.generate_initial_guesses_v_field()
    ny = simple.mesh.ny
    nx = simple.mesh.nx

    for j in range(ny + 1):  # v has ny+1 rows
        for i in range(nx + 2):  # v has nx+2 columns
            v = simple.mesh.v_nodes[j][i].v_old
            if j == 0 or j == ny:
                assert v == 0.0, f"Top/bottom boundary failed at v[{j}][{i}] = {v}"
            else:
                assert v == 0.0001, f"Interior value wrong at v[{j}][{i}] = {v}"

def test_simple_generate_initial_guesses_p_field_is_correct_and_didnt_change_boundaries(simple): 
    simple.generate_initial_guesses_p_field()
    ny = simple.mesh.ny
    nx = simple.mesh.nx - 1  # pressure has nx-1 columns

    for j in range(ny):
        for i in range(nx):
            p = simple.mesh.p_nodes[j][i].p_old
            assert p == 0.001, f"p[{j}][{i}] = {p}, expected 0.001"


def test_simple_generate_initial_guesses(simple):
    simple.generate_initial_guesses()
    assert simple.mesh.u_nodes[0][0].u_old == 0.001
    assert simple.mesh.v_nodes[1][0].v_old == 0.0001
    assert simple.mesh.p_nodes[0][0].p_old == 0.001
    assert simple.mesh.u_nodes[0][4].u_old == .001







def test_first_iteration_calculate_u_field(simple):
    simple.generate_initial_guesses()
    A,b = simple.calculate_u_field()
    expected_A = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-0.0027, 0.0358, -0.0002, 0, 0, -0.005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -0.0027, 0.0358, -0.0002, 0, 0, -0.005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, -0.0027, 0.0358, -0.0002, 0, 0, -0.005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-0.0063, 0, 0, 0, 0, -0.0027, 0.0283, -0.0002, 0, 0, -0.005, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -0.0063, 0, 0, 0, -0.0027, 0.0283, -0.0002, 0, 0, 0, -0.005, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, -0.0063, 0, 0, 0, -0.0027, 0.0283, -0.0002, 0, 0, 0, -0.005, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-0.0063, 0, 0, 0, 0, 0, -0.0027, 0.0283, -0.0002, 0, 0, 0, 0, -0.005, 0, 0, 0, 0, 0, 0],
        [0, -0.0063, 0, 0, 0, 0, -0.0027, 0.0283, -0.0002, 0, 0, 0, 0, 0, -0.005, 0, 0, 0, 0, 0],
        [0, 0, -0.0063, 0, 0, 0, 0, -0.0027, 0.0283, -0.0002, 0, 0, 0, 0, 0, -0.005, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, -0.0063, 0.0283, -0.0002, 0, 0, 0, 0, 0, 0, -0.005, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -0.0063, 0.0283, -0.0002, 0, 0, 0, 0, 0, 0, -0.005, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, -0.0063, 0.0383, -0.0002, 0, 0, 0, 0, 0, 0, -0.005, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.0063, 0.0383, -0.0002, 0, 0, 0, 0, 0, 0, -0.005],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.0063, 0.0383, -0.0002, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.0063, 0.0383, -0.0002, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1]
    ])

    expected_b = np.array([
        0.001, 1.79E-5, 1.79E-5, 1.79E-5, 0.0,
        0.001, 1.42E-5, 1.42E-5, 1.42E-5, 0.0,
        0.001, 1.42E-5, 1.42E-5, 1.42E-5, 0.0,
        0.001, 1.92E-5, 1.92E-5, 1.92E-5, 0.0
    ])

    assert A.shape == expected_A.shape
    assert b.shape == expected_b.shape
    # assert np.allclose(A, expected_A, atol=1e-6)
    assert np.allclose(b, expected_b, atol=1e-8)