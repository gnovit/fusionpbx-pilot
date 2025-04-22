import pytest
@pytest.mark.dependency(depends=['test_domain_list'])
def test_domains_list(fusionpbx):
    domains = fusionpbx.domains.list()

    assert len(domains) > 0, "Find at least one domain"
    assert isinstance(domains, list), "Domains should be a list"
    assert all(isinstance(domain, dict) for domain in domains), (
        "Each domain should be a dictionary"
    )
    assert any(domain.get("name") == "fusionpbx-pilot.pytest" for domain in domains), (
        "Find domain 'fusionpbx-pilot.pytest'"
    )

    assert any(domain.get("name") == "fusionpbx1-pilot.pytest" for domain in domains), (
        "Find domain 'fusionpbx1.pytest'"
    )
