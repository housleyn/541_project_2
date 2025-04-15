from node import Node 
import pytest 

@pytest.fixture
def node():
    return Node()

def test_given_node_initialization_is_correct(node):
    assert node.p_old == 0.0
    assert node.p == 0.0
    assert node.aP == 0.0
    assert node.aE == 0.0
    assert node.aW == 0.0
    assert node.aN == 0.0
    assert node.aS == 0.0
    assert node.b == 0.0
    assert node.position is None

def test_given_node_position_is_set_correctly(node):
    node.position = (1, 2)
    assert node.position == (1, 2)

def test_given_node_pressure_is_set_correctly(node):
    node.p = 1000.0
    assert node.p == 1000.0

def test_given_node_pressure_old_is_set_correctly(node):
    node.p_old = 500.0
    assert node.p_old == 500.0

def test_given_node_coefficients_are_set_correctly(node):
    node.aP = 1.0
    node.aE = 0.5
    node.aW = 0.5
    node.aN = 0.25
    node.aS = 0.25
    node.b = 10.0

    assert node.aP == 1.0
    assert node.aE == 0.5
    assert node.aW == 0.5
    assert node.aN == 0.25
    assert node.aS == 0.25
    assert node.b == 10.0

def test_given_node_define_pressure_coefficients_is_correct(node):
    rho = 1.0
    dx = 0.1
    dy = 0.2
    uE = 2.0
    uW = 1.0
    vN = 1.5
    vS = 0.5
    dE = 0.25
    dW = 0.25
    dN = 0.5
    dS = 0.5

    node.define_pressure_correction_coefficients(rho, dx, dy, uE, uW, vN, vS, dE, dW, dN, dS)

    assert node.aE == pytest.approx(rho * dE * dy)
    assert node.aW == pytest.approx(rho * dW * dy)
    assert node.aN == pytest.approx(rho * dN * dx)
    assert node.aS == pytest.approx(rho * dS * dx)
    assert node.aP == pytest.approx(node.aE + node.aW + node.aN + node.aS)
    expected_b = rho * (-uE*dy + uW*dy - vN*dx + vS*dx)
    assert node.b == pytest.approx(expected_b)