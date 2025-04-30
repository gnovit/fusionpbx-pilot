def test_extensions_list(fusionpbx):
    extensions = fusionpbx.domain('fusionpbx-pilot.pytest').extensions.list()

    assert len(extensions) > 0, 'Find at least one extension'
    assert isinstance(extensions, list), 'Extensions should be a list'
    assert all(isinstance(extension, dict) for extension in extensions), (
        'Each Extension should be a dictionary'
    )
    assert any(extension.get('name') == '1000' for extension in extensions), (
        "Find extension '1000'"
    )
