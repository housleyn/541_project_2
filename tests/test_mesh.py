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
    return mesh

def test_given_mesh_domain_is_initialized_correctly(mesh):
    assert mesh.domain.lower_boundary_func(0, 0) == 0
    assert mesh.domain.upper_boundary_func(0, 0) == 0.01
    assert mesh.domain.left_boundary_func(0) == 0
    assert mesh.domain.right_boundary_func(0) == 0.05


def test_given_mesh_then_initialization_is_correct(mesh):
    assert mesh.nx == 4
    assert mesh.ny == 4
    assert mesh.dx == .0125
    assert mesh.dy == .0025

def test_given_mesh_then_p_node_size_and_values_are_correct(mesh):
    assert len(mesh.p_nodes) == mesh.ny
    assert len(mesh.p_nodes[0]) == mesh.nx
    assert all(len(row) == mesh.nx for row in mesh.p_nodes)
    assert all(all(node is None for node in row) for row in mesh.p_nodes)

def test_given_mesh_then_u_node_size_and_values_are_correct(mesh):
    assert len(mesh.u_nodes) == 4
    assert len(mesh.u_nodes[0]) == 5
    assert all(len(row) == mesh.nx + 1 for row in mesh.u_nodes)
    assert all(all(node is None for node in row) for row in mesh.u_nodes)

def test_given_mesh_then_v_node_size_and_values_are_correct(mesh):
    assert len(mesh.v_nodes) == 5
    assert len(mesh.v_nodes[0]) == 6
    assert all(len(row) == mesh.nx + 2 for row in mesh.v_nodes)
    assert all(all(node is None for node in row) for row in mesh.v_nodes)

def test_given_mesh_construct_methods_exist(mesh):
    assert hasattr(mesh, 'construct_u_mesh')
    assert hasattr(mesh, 'construct_v_mesh')
    assert hasattr(mesh, 'construct_p_mesh')


def test_integration_between_node_class_and_mesh(mesh):
    mesh.construct_p_mesh()
    assert mesh.p_nodes[0][0].p == 0.0
    assert mesh.p_nodes[0][1].p == 0.0
    assert mesh.p_nodes[1][0].p == 0.0


def test_given_meseh_construct_u_mesh_integration_with_control_surfaces(mesh):
    mesh.construct_u_mesh()
    assert mesh.u_nodes[0][0].u == None
    assert mesh.u_nodes[0][1].u == None
    assert mesh.u_nodes[1][0].u == None

def test_given_mesh_construct_v_mesh_integration_with_node(mesh):
    mesh.construct_v_mesh()
    assert mesh.v_nodes[0][0].v == None
    assert mesh.v_nodes[0][1].v == None
    assert mesh.v_nodes[1][0].v == None

def test_construct_p_nodes_gives_correct_position(mesh):
    mesh.construct_p_mesh()
    assert mesh.p_nodes[0][0].position == pytest.approx((0.00625, 0.00125))
    assert mesh.p_nodes[1][1].position == pytest.approx((0.01875, 0.00375))
    assert mesh.p_nodes[3][3].position == pytest.approx((0.04375, 0.00875))

def test_construct_u_nodes_gives_correct_positions(mesh):
    mesh.construct_u_mesh()
    assert mesh.u_nodes[0][0].position == pytest.approx((0.0, 0.00125))
    assert mesh.u_nodes[1][1].position == pytest.approx((0.0125, 0.00375))
    assert mesh.u_nodes[3][4].position == pytest.approx((0.05, 0.00875))

def test_construct_v_nodes_gives_correct_positions(mesh):
    mesh.construct_v_mesh()
    assert mesh.v_nodes[0][0].position == pytest.approx((-.00625, 0.0))
    assert mesh.v_nodes[0][1].position == pytest.approx((0.00625, 0.0))
    assert mesh.v_nodes[1][1].position == pytest.approx((0.00625, 0.0025))
    assert mesh.v_nodes[4][5].position == pytest.approx((0.05625, 0.01))
    
def test_index_algebra_between_meshes_is_correct(mesh):
    mesh.construct_u_mesh()
    mesh.construct_v_mesh()
    mesh.construct_p_mesh()
    u_pos = mesh.u_nodes[0][1].position
    v_pos = mesh.v_nodes[0][1].position
    p_pos = mesh.p_nodes[0][1].position

    sum_x = u_pos[0] + v_pos[0] + p_pos[0]
    sum_y = u_pos[1] + v_pos[1] + p_pos[1]

    assert (sum_x, sum_y) == pytest.approx((0.0375, 0.0025))



def test_construct_mesh_works(mesh):
    mesh.construct_mesh()

    u_pos = mesh.u_nodes[0][0].position
    v_pos = mesh.v_nodes[0][1].position
    p_pos = mesh.p_nodes[0][0].position

    sum_x = u_pos[0] + v_pos[0] + p_pos[0]
    sum_y = u_pos[1] + v_pos[1] + p_pos[1]

    assert (sum_x, sum_y) == pytest.approx((0.0125, 0.0025))

def test_build_matrix_returns_correct_sizes(mesh):
    mesh.construct_mesh()
    A, b = mesh.build_matrix(mesh.p_nodes)
    assert A.shape == (mesh.nx * mesh.ny, mesh.nx * mesh.ny)
    assert b.shape == (mesh.nx * mesh.ny,)