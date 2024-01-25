"""
Delete all domains except the ones in the FORGET list.
Make sure to add domain_delete permission to the user you are using to run this script on FusionPBX interface
on Advanced/Group Manager/Permissions/ for Superadmin group or group of user that will be used to run this script.
"""

from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX

browser = Firefox()

# Domains to be kept
FORGET = ["domain.com", "172.17.0.1", "another.domain.com"]

url = "pbx.domain.com"        # URL of your FusionPBX
user = "pilot"                # User with superadmin privileges
password = "C0mpl3xP4ssw0rd"  # Password for the user

f = FusionPBX(browser, url, user, password)

all_domains = f.domains.list()

for d in all_domains:
    if d['name'] not in FORGET:
        print(f"Deleting Domain: {d['name']}")
        domain = f.domain(d['name'])
        del domain.name
    else:
        print(f"Skipping Domain: {d['name']}")

browser.quit()
