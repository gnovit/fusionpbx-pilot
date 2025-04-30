import pytest

from fusionpbx_pilot.page_objects.apps.extension import ExtensionNotFound


def test_extension_get_unexisting(fusionpbx):
    """Test to get a extension that does not exist."""
    with pytest.raises(ExtensionNotFound) as excinfo:
        fusionpbx.domain('fusionpbx-pilot.pytest').extension('unexisting-extension')
    assert str(excinfo.value) == 'Extension unexisting-extension not found', (
        'Should raise ExtensionNotFound exception'
    )


@pytest.mark.dependency()
def test_extension_create(fusionpbx):
    e = fusionpbx.domain('fusionpbx-pilot.pytest').extension(
        'test-extension', create=True
    )
    assert e.name == 'test-extension', 'Domain name should be test-extension'


@pytest.mark.dependency(depends=['test_extension_create'])
def test_change_and_get_password(fusionpbx):
    e = fusionpbx.domain('fusionpbx-pilot.pytest').extension('test-extension')
    e.password = 'test-password'
    assert e.password == 'test-password', 'Password should be test-password'


@pytest.mark.dependency(depends=['test_extension_create'])
def test_change_and_get_voicemail_enabled(fusionpbx):
    e = fusionpbx.domain('fusionpbx-pilot.pytest').extension('test-extension')
    e.voicemail_enabled = True
    assert e.voicemail_enabled, 'voicemail_enabled should be True'
    e.voicemail_enabled = False
    assert not e.voicemail_enabled, 'voicemail_enabled should be False'


@pytest.mark.dependency(depends=['test_extension_create'])
def test_change_and_get_voicemail_mail_to(fusionpbx):
    e = fusionpbx.domain('fusionpbx-pilot.pytest').extension('test-extension')
    e.voicemail_mail_to = 'test-user@pytest'
    assert e.voicemail_mail_to == 'test-user@pytest', (
        'voicemail_mail_to should be test-user@pytest'
    )

@pytest.mark.dependency()#depends=['test_extension_create', 'test_change_and_get_voicemail_mail_to', 'test_change_and_get_voicemail_enabled', 'test_change_and_get_password',])
def test_extension_delete(fusionpbx):
    e = fusionpbx.domain('fusionpbx-pilot.pytest').extension('test-extension')
    del e.name
    with pytest.raises(ExtensionNotFound) as excinfo:
        fusionpbx.domain('fusionpbx-pilot.pytest').extension('test-extension')
    assert str(excinfo.value) == 'Extension test-extension not found', (
        'Should raise ExtensionNotFound exception'
    )