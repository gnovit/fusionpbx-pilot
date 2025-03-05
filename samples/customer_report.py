"""
This script will list all extensions on a domain or subdomain :wqbased on text passed to the script by command line.
copy samples/.env.sample to samples/.env and fill the values with your FusionPBX credentials.
Ex.
python samples/customer_report.py 'mydomain.com'
python samples/customer_report.py '.com'
"""

from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX

from dotenv import dotenv_values
import sys


config = dotenv_values("samples/.env")

DOMAIN = sys.argv[1]

browser = Firefox()


f = FusionPBX(browser, config["URL"], config["USER"], config["PASSWORD"])

domains = f.domains.list()
customer_total_domains = 0
customer_total_extensions = 0
for domain in domains:
    if DOMAIN in domain["name"]:
        customer_total_domains += 1
        print(f"Domain: {domain['name']}")
        d = f.domain(domain["name"])
        extensions = d.extensions.list()
        domain_total_extensions = len(extensions)
        for e in extensions:
            print(f"Extension: {e['name']}")
        print(f"Total for this domain:  {domain_total_extensions}")
        customer_total_extensions += domain_total_extensions
print(f"Total domains for customer {DOMAIN}: {customer_total_domains}")
print(f"Total extensions for customer {DOMAIN}: {customer_total_extensions}")
