from domain import Domain 
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


def test_given_domain_boundaries_are_callable(domain):
    assert callable(domain.lower_boundary_func)
    assert callable(domain.upper_boundary_func)
    assert callable(domain.left_boundary_func)
    assert callable(domain.right_boundary_func)

def test_given_domain_bounds_are_correct(domain):
    x_range, y_range = domain.get_bounds()
    assert x_range == (0, .05)
    assert y_range == (0, .01)

def test_when_plot_is_called_it_runs(domain):
    x_range, y_range = domain.get_bounds()
    domain.plot_domain(x_range, y_range)
    assert True