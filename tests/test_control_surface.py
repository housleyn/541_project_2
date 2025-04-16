from control_surfaces import ControlSurface
import pytest


@pytest.fixture
def control_surface():
    control_surface = ControlSurface()
    control_surface.u_old = 1.0
    control_surface.v_old = 2.0
    
    return control_surface

def test_control_surface_initialization(control_surface):
    assert control_surface.u is None
    assert control_surface.v is None
    assert control_surface.u_old == 1.0
    assert control_surface.v_old == 2.0
    assert control_surface.position is None
    assert control_surface.b is None
    assert control_surface.aE is None
    assert control_surface.aW is None
    assert control_surface.aN ==None
    assert control_surface.aS is None
    assert control_surface.aP is None

def test_given_control_surface_methods(control_surface):
    assert hasattr(control_surface, 'calculate_x_coefficients')
    assert hasattr(control_surface, 'calculate_y_coefficients')






def test_calculate_x_coefficients_interior_node_E(control_surface):
    cs = control_surface
    cs.u_old = 0.001
    mu = 0.001
    rho = 1000
    dx = .0125
    dy = .0025
    uE_old = .001
    uW_old = .001
    Fe = rho / 2 * (uE_old + cs.u_old)
    De = mu/dx
    aE = De*dy + max(-Fe, 0)*dy 
    assert aE == pytest.approx(.0002)