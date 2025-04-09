FusionPBX Pilot Python Library
==============================

[Gnovit](https://www.gnovit.com)

email: fusionpbx-pilot@gnovit.com

This python library is intended to automate [FusionPBX](https://www.fusionpbx.com) administrative tasks.
This library is based on Selenium WebDriver and abstracts FusionPBX objects as python objects.
Shold be used in an API to manage FusionPBX.
This is licensed under the terms of the GNU GPL v3 license.

Examples
--------

Install the library:

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install fusionpbx-pilot
```

Instantiate the FusionPBX class:

``` python
from selenium.webdriver import Firefox
from fusionpbx_pilot.page_objects import FusionPBX
f = FusionPBX(Firefox(), '<https://addr>', '<login_user>', '<login_password>')
```

- Set domain object: If domain no exist, create it, returning existing domain object:

``` python
d = f.domain('<domain_name>')
```

Domain manipulate
--------------------

- Domain rename:

``` python
d.name = '<new_domain_name>'
```

- Domain get uuid:

``` python
d.uuid
```

- Domain delete:
  *You must to add domain delete permission to the user used to login to FusionPBX.*
  
``` python
del f.domain.name
```

Extensions manipulate
--------------------
  
- List all extensions of a domain:

``` python
d.extensions.list()
```

- Set or create a extension object:
  
``` python
e = d.extension('<extension_name>')
```

Generally extension name is a number...

If extension no exist, the lib will create it.

- Rename extension object

``` python
e.name = '<new_extension_name>'
```

- Get or set password

``` python
e.password
```

Returns password

``` python
e.password = '<new_password>'
```

Set the password

- Get or set voicemail enabled:

``` python
e.voicemail_enabled
```

- Get or set voicemail_mail_to:

``` python
e.voicemail_mail_to
```

- Get UUID:

``` python
e.uuid
```

- Delete extension

``` python
del d.extension.name
```




Contributions
-------------

Contribuitions are welcome.
Please fork the project and send a pull request.
