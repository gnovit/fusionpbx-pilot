import pytest

@pytest.mark.dependency()
def test_domain_create(fusionpbx):
    d = fusionpbx.domain("fusionpbx1.pytest")
    assert d.name == "fusionpbx1.pytest", "Domain name should be 'fusionpbx1.pytest'"


@pytest.mark.dependency(depends=["test_domain_create"])
def test_domain_get(fusionpbx):
    d = fusionpbx.domain("fusionpbx1-pilot.pytest")

    assert d.name == "fusionpbx1-pilot.pytest", (
        "Domain name should be 'fusionpbx1.pytest'"
    )

@pytest.mark.order(after="test_domain_get")
def test_domain_delete(fusionpbx):
    d = fusionpbx.domain("fusionpbx1.pytest")
    del d.name
    assert ()
    
    )