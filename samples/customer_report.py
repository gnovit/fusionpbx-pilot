"""
This script will list all extensions on a domain or subdomain based on text passed to the script by command line.
copy samples/.env.sample to samples/.env and fill the values with your FusionPBX credentials.
Ex.
python samples/customer_report.py 'mydomain.com'
python samples/customer_report.py '.com'
"""

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from pilot.page_objects import FusionPBX



from dotenv import dotenv_values
import sys

from fpdf import FPDF
from datetime import datetime
from weasyprint import HTML

options = Options()
options.add_argument("--headless")

config = dotenv_values(".env")

DOMAIN = sys.argv[1]

browser = Firefox(options=options)


f = FusionPBX(browser, config["URL"], config["USER"], config["PASSWORD"])

domains = f.domains.list()
base_total_extensions = 0 
sub_total_domains = 0
sub_total_extensions = 0
header = """<!DOCTYPE html>
<html>
<head>
    <style>
        table,
        th,
        td {
            border: 1px solid black;
            border-collapse: collapse;
            padding: 6px;
        }
    </style>
    <p>
        <img src='img/logo.png' alt='Logo' align=right style='width:25%;'>
    </p>
</head>
 """

header += "<h1>gnovit.net Cloud Telephony Customer Report</h1>\n"
header += f"<h2>Date: {datetime.now().strftime('%d/%m/%Y')}</h2>\n"
header += f"<h2>Domain: {DOMAIN}</h2>\n"

base_domain_report = []
base_domain_report.append("<table>")
base_domain_report.append("<tr><th colspan='3'> Base Domain</th></tr>")
base_domain_report.append("<tr><th align='left'>Name</th><th align='center'>Description</th align='right'><th>Extensions</th></tr>")

sub_domains_report = []
sub_domains_report.append("<table>")
sub_domains_report.append("<tr><th colspan='3'> Sub Domains (condominium)</th></tr>")
sub_domains_report.append("<tr><th align='left'>Name</th><th align='center'>Description</th align='right'><th>Extensions</th></tr>")

for domain in domains:
    if DOMAIN == domain["name"] :
        print(f"Processing {domain['name']}")
        d = f.domain(domain["name"])
        extensions = d.extensions.list()
        base_total_extensions = len(extensions)
        base_domain_report.append(f"<tr><td align='left'>{domain['name']}</td><td align='center'>{domain['description']}</td><td align='right'>{base_total_extensions}</td></tr>")

    elif DOMAIN in domain["name"] and config['EXCLUDE_DOMAINS'] not in domain["name"]:
        print(f"Processing {domain['name']}")
        d = f.domain(domain["name"])
        extensions = d.extensions.list()
        domain_total_extensions = len(extensions)
        sub_total_domains += 1
        sub_total_extensions += domain_total_extensions
        sub_domains_report.append(f"<tr><td align='center'>{domain['name']}</td><td align='center'>{domain['description']}</td><td align='right'>{domain_total_extensions}</td></tr>")

base_domain_report.append("<tr><th align='center' colspan='3'>Total</th></tr>")
base_domain_report.append(f"<tr><th colspan='2'>1</th><th align='right'>{base_total_extensions}</th></tr>")
base_domain_report.append("</table>")
base_domain_report.append("<p></p>")

sub_domains_report.append("<tr><th align='center' colspan='3'>Total</th></tr>")
sub_domains_report.append(f"<tr><td align='center' colspan='2'> {sub_total_domains}</td><td align='right'>{sub_total_extensions}</td></tr>")
sub_domains_report.append("</table>")

print('Generating customer_report.html')
with open("customer_report.html", "w") as file:
    file.write(header)
    file.write("\n".join(base_domain_report))
    file.write("\n".join(sub_domains_report))

print('Converting customer_report.html to PDF')
HTML('customer_report.html').write_pdf('customer_report.pdf')

browser.quit()
