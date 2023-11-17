 FusionPBX Pilot library
* ========================
  

Examples:

Instantiate the FusionPBX class

.. code python
    from selenium.webdriver import Firefox
    from pilot.page_objects import FusionPBX

    f = FusionPBX(Firefox(), <https:://addr>, <login_user>, <login_password>)

- Set domain object:
  If domain no exist, create it, esle return existing domain object:
  .. code python
      d = f.domain = <domain_name>

- Domain rename:
.. .. code python
..     d.name = <new_domain_name>

- Domain delete:
  .. code python
      del d.domain.name

Extensions manipulate:
- Set extension object:
  .. code python
      e = d.extension = <extension_number>