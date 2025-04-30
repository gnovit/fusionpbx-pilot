def test_domains_list(fusionpbx):
    domains = fusionpbx.domains.list()

    assert len(domains) > 0, 'Find at least one Domain'
    assert isinstance(domains, list), 'Domains should be a list'
    assert all(isinstance(domain, dict) for domain in domains), (
        'Each Domain should be a dictionary'
    )
    assert any(domain.get('name') == 'fusionpbx-pilot.pytest' for domain in domains), (
        "Find domain 'fusionpbx-pilot.pytest'"
    )