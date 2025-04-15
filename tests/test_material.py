from material import Material
import pytest 

@pytest.fixture
def material():
    material = Material()
    material.rho = 1.0
    material.mu = 0.01
    return material

def test_initalizing_material_is_correct(material):
    assert material.rho == 1.0
    assert material.mu == 0.01