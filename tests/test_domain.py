import pytest

from fusionpbx_pilot.page_objects.core.domain import DomainNotFound


def test_get_domain_from_1st_run(fusionpbx):
    """Test to get a domain from the first run."""
    d = fusionpbx.domain('fusionpbx-pilot.pytest')
    assert d.name == 'fusionpbx-pilot.pytest', (
        "Domain name should be 'fusionpbx-pilot.pytest'"
    )


def test_domain_get_unexisting(fusionpbx):
    """Test to get a domain that does not exist."""
    with pytest.raises(DomainNotFound) as excinfo:
        fusionpbx.domain('nonexistent-domain.pytest')
    assert str(excinfo.value) == 'Domain nonexistent-domain.pytest not found', (
        'Should raise DomainNameNotFound exception'
    )


@pytest.mark.dependency()
def test_domain_create(fusionpbx, test_domain):
    d = fusionpbx.domain(test_domain, create=True)
    assert d.name == test_domain, f'Domain name should be {test_domain}'


@pytest.mark.dependency(depends=['test_domain_create'])
def test_domain_change_n_get_existing(fusionpbx, test_domain):
    d = fusionpbx.domain(test_domain)

    assert d.name == test_domain, f'Domain name should be {test_domain}'


@pytest.mark.order(after='test_domain_change_n_get_existing')
def test_domain_delete(fusionpbx, test_domain):
    d = fusionpbx.domain(test_domain)
    del d.name

    with pytest.raises(DomainNotFound) as excinfo:
        fusionpbx.domain(test_domain)
    assert str(excinfo.value) == f'Domain {test_domain} not found', (
        'Should raise DomainNameNotFound exception'
    )


@pytest.mark.order(before='test_domain_delete')
@pytest.mark.dependency(depends=['test_domain_create'])
def test_domain_rename(fusionpbx, test_domain):
    d = fusionpbx.domain(test_domain)
    new_name = f'{test_domain}-renamed'
    d.name = new_name
    assert d.name == new_name, f'Domain name should be {new_name}'
    d.name = test_domain
    assert d.name == test_domain, f'Domain name should be {test_domain}'
