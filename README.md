FusionPBX Pilot Python Library
==============================

Gnovit
https://www.gnovit.com

fusionpbx-pilot@gnovit.com

This python library is intended to automate FusionPBX administration tasks.
This library is based on Selenium WebDrive and abstracts FusionPBX apps as python objects.
Shold be used in an API to manage FusionPBX.
This is licensed under the terms of the GNU GPL v3 license.

Examples
--------

Instantiate the FusionPBX class:

``` python
from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX
f = FusionPBX(Firefox(), <https://addr>, <login_user>, <login_password>)
```

- Set domain object: If domain no exist, create it, returning existing domain object:

``` python
d = f.domain = <domain_name>
```

Domain manipulate
--------------------

- Domain rename:

``` python
d.name = <new_domain_name>
```

- Domain delete:
  
``` python
del d.domain.name
```

Extensions manipulate
--------------------
  
- Set extension object:
  
``` python
e = d.extension = <extension_number>
```

C0mpl3xP4ssw0rd