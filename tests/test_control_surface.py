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

def test_calculate_x_coefficients(control_surface):
    cs = control_surface
    mu = 0.01
    rho = 1.0
    dx = 0.1
    dy = 0.2
    alphau = 0.7
    pe = 1.0
    pw = 0.0
    uE_old = 1.2
    uW_old = 0.8
    vUL_old = 0.5
    vUR_old = 0.5
    vBL_old = 0.5
    vBR_old = 0.5
    i=1
    nx=4

    cs.calculate_x_coefficients(mu, rho, dx, dy, alphau, pe, pw,
                                 uE_old, uW_old, vUL_old, vUR_old, vBL_old, vBR_old,i,nx)

    # Validate coefficient structure
    assert cs.aE >= 0
    assert cs.aW >= 0
    assert cs.aN >= 0
    assert cs.aS >= 0
    assert cs.aP == pytest.approx(cs.aE + cs.aW + cs.aN + cs.aS + 
                                  (rho/2 * (uE_old + cs.u_old) - rho/2 * (uW_old + cs.u_old)) * dy +
                                  (rho/2 * (vUL_old + vUR_old) - rho/2 * (vBL_old + vBR_old)) * dx)

    expected_b = (pw - pe) * dy + ((1 - alphau) / alphau) * cs.aP * cs.u_old
    assert cs.b == pytest.approx(expected_b)

def test_calculate_y_coefficients(control_surface):
    cs = control_surface
    mu = 0.01
    rho = 1.0
    dx = 0.1
    dy = 0.2
    alphav = 0.6
    ps = 0.5
    pn = 1.5
    vN_old = 2.2
    vS_old = 1.8
    uUL_old = 0.9
    uUR_old = 1.1
    uBL_old = 0.8
    uBR_old = 1.2

    cs.calculate_y_coefficients(mu, rho, dx, dy, alphav, ps, pn,
                                 vN_old, vS_old, uUL_old, uUR_old, uBL_old, uBR_old)

    # Validate coefficient structure
    assert cs.aE >= 0
    assert cs.aW >= 0
    assert cs.aN >= 0
    assert cs.aS >= 0
    assert cs.aP == pytest.approx(cs.aE + cs.aW + cs.aN + cs.aS + 
                                  (rho/2 * (uUR_old + uBR_old) - rho/2 * (uUL_old + uBL_old)) * dy +
                                  (rho/2 * (vN_old + cs.v_old) - rho/2 * (vS_old + cs.v_old)) * dx)

    expected_b = (ps - pn) * dx + ((1 - alphav) / alphav) * cs.aP * cs.v_old
    assert cs.b == pytest.approx(expected_b)