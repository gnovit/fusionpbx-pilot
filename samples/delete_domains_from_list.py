"""
Delete all domains except the ones in the FORGET list.
Make sure to add domain_delete permission to the user you are using to run this script on FusionPBX interface
on Advanced/Group Manager/Permissions/ for Superadmin group or group of user that will be used to run this script.
"""

from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX
from dotenv import dotenv_values

browser = Firefox()

config = dotenv_values(".env")

# Domains to be kept
FORGET = ["domain.com", "172.17.0.1", "another.domain.com"]

f = FusionPBX(browser, config["URL"], config["USER"], config["PASSWORD"])

all_domains = f.domains.list()

for d in all_domains:
    if d['name'] not in FORGET:
        print(f"Deleting Domain: {d['name']}")
        domain = f.domain(d['name'])
        del domain.name
    else:
        print(f"Skipping Domain: {d['name']}")

browser.quit()
