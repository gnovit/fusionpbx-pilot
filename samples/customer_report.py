"""
This script will Create a html and pdf report of all extensions on a domain and its subdomains based on text passed to the script by command line.
copy samples/.env.sample to samples/.env and fill the values with your FusionPBX credentials.
Ex.
python samples/customer_report.py 'mydomain.com'
python samples/customer_report.py '.com'
python samples/customer_report.py domain.com -e sub1 -e sub2
"""

import os
from datetime import datetime
from typing import List, Optional

import typer
from dotenv import dotenv_values
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from weasyprint import HTML

from fusionpbx_pilot.page_objects import FusionPBX

app = typer.Typer()


@app.command()
def main(
    domain: str = typer.Argument(..., help='Domain to generate report for'),
    exclude: Optional[List[str]] = typer.Option(
        None,
        '-e',
        '--exclude',
        help='Subdomains to exclude from report (can be used multiple times)',
    ),
    exclude_extension: Optional[List[str]] = typer.Option(
        None,
        '-x',
        '--exclude-extension',
        help='Extensions to exclude from report by number/name (can be used multiple times)',
    ),
    url: Optional[str] = typer.Option(
        None, '--url', help='FusionPBX URL (overrides env var and .env)'
    ),
    user: Optional[str] = typer.Option(
        None, '--user', help='FusionPBX username (overrides env var and .env)'
    ),
    password: Optional[str] = typer.Option(
        None, '--password', help='FusionPBX password (overrides env var and .env)'
    ),
):
    """
    Generate a HTML and PDF report of all extensions on a domain and its subdomains.
    """
    # Load .env file
    config = dotenv_values('.env')

    # Configuration priority: CLI args > env vars > .env file
    # Use FUSIONPBX_* prefix for env vars to avoid conflicts (e.g., USER is system username)
    # For backward compatibility, also check generic names, but skip USER env var (always system user)
    fusionpbx_url = (
        url or os.getenv('FUSIONPBX_URL') or os.getenv('URL') or config.get('URL')
    )
    fusionpbx_user = user or os.getenv('FUSIONPBX_USER') or config.get('USER')
    fusionpbx_password = (
        password
        or os.getenv('FUSIONPBX_PASSWORD')
        or os.getenv('PASSWORD')
        or config.get('PASSWORD')
    )

    # Get EXCLUDE_DOMAINS from .env if present (for backward compatibility)
    exclude_domains_from_env_raw = config.get('EXCLUDE_DOMAINS', '')
    # Parse comma, space separated, or Python list format from .env
    exclude_domains_env_list = []
    if exclude_domains_from_env_raw:
        # Try to parse as Python list format first (e.g., ['default','public'] or ["default","public"])
        exclude_domains_str = exclude_domains_from_env_raw.strip()
        if exclude_domains_str.startswith('[') and exclude_domains_str.endswith(']'):
            # Python list format - remove brackets and parse
            inner = exclude_domains_str[1:-1].strip()
            if inner:
                # Split by comma and clean up quotes and whitespace
                exclude_domains_env_list = [
                    dom.strip().strip("'\"") for dom in inner.split(',')
                ]
        elif ',' in exclude_domains_from_env_raw:
            # Comma-separated format
            exclude_domains_env_list = [
                dom.strip() for dom in exclude_domains_from_env_raw.split(',')
            ]
        else:
            # Space-separated or single value format
            exclude_domains_env_list = exclude_domains_from_env_raw.split()

    # Get EXCLUDE_EXTENSIONS from .env if present
    exclude_extensions_from_env = config.get('EXCLUDE_EXTENSIONS', '')
    # Parse comma, space separated, or Python list format from .env
    exclude_extensions_env_list = []
    if exclude_extensions_from_env:
        # Try to parse as Python list format first (e.g., ['1099','1098'] or ["1099","1098"])
        exclude_extensions_str = exclude_extensions_from_env.strip()
        if exclude_extensions_str.startswith('[') and exclude_extensions_str.endswith(']'):
            # Python list format - remove brackets and parse
            inner = exclude_extensions_str[1:-1].strip()
            if inner:
                # Split by comma and clean up quotes and whitespace
                exclude_extensions_env_list = [
                    ext.strip().strip("'\"") for ext in inner.split(',')
                ]
        elif ',' in exclude_extensions_from_env:
            # Comma-separated format
            exclude_extensions_env_list = [
                ext.strip() for ext in exclude_extensions_from_env.split(',')
            ]
        else:
            # Space-separated format
            exclude_extensions_env_list = exclude_extensions_from_env.split()

    # Combine exclude lists from CLI and .env
    exclude_list = exclude or []
    # Combine CLI and .env domain exclude lists
    all_exclude_domains = list(set(exclude_list + exclude_domains_env_list))
    
    exclude_extension_list = exclude_extension or []
    # Combine CLI and .env extension exclude lists
    all_exclude_extensions = list(set(exclude_extension_list + exclude_extensions_env_list))

    if not fusionpbx_url or not fusionpbx_user or not fusionpbx_password:
        typer.echo(
            'Error: URL, USER, and PASSWORD must be provided via CLI, environment variables, or .env file',
            err=True,
        )
        raise typer.Exit(1)

    options = Options()
    options.add_argument('--headless')

    browser = Firefox(options=options)

    f = FusionPBX(browser, fusionpbx_url, fusionpbx_user, fusionpbx_password)

    # Log excluded extensions if any are configured
    if all_exclude_extensions:
        print(f'Excluding extensions: {", ".join(all_exclude_extensions)}')
        print('')

    domains = f.domains.list()
    base_total_extensions = 0
    base_domain_found = False
    base_domain_description = ''
    sub_total_domains = 0
    sub_total_extensions = 0

    # Helper function to filter excluded extensions
    def filter_extensions(extensions_list, exclude_list):
        """Filter out excluded extensions from the list."""
        if not exclude_list:
            return extensions_list
        filtered = []
        excluded_extensions = []
        for ext in extensions_list:
            # Extensions are dictionaries with a 'name' field
            ext_name = ext.get('name', '')
            if ext_name not in exclude_list:
                filtered.append(ext)
            else:
                excluded_extensions.append(ext_name)
        if excluded_extensions:
            print(f'  Excluded {len(excluded_extensions)} extension(s): {", ".join(excluded_extensions)}')
        return filtered
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

    header += '<h1>Customer Report</h1>\n'
    header += f'<h2>Date: {datetime.now().strftime("%d/%m/%Y")}</h2>\n'
    header += f'<h2>Domain: {domain}</h2>\n'

    base_domain_report = []
    base_domain_report.append('<table>')
    base_domain_report.append("<tr><th colspan='3'> Base Domain</th></tr>")
    base_domain_report.append(
        "<tr><th align='left'>Name</th><th align='center'>Description</th align='right'><th>Extensions</th></tr>"
    )

    sub_domains_report = []
    sub_domains_report.append('<table>')
    sub_domains_report.append("<tr><th colspan='3'> Sub Domains</th></tr>")
    sub_domains_report.append(
        "<tr><th align='left'>Name</th><th align='center'>Description</th align='right'><th>Extensions</th></tr>"
    )

    for domain_item in domains:
        # Check if domain should be excluded
        should_exclude = False
        exclude_reason = None
        if all_exclude_domains:
            for exclude_domain in all_exclude_domains:
                if exclude_domain in domain_item['name']:
                    should_exclude = True
                    # Determine if excluded by CLI or .env
                    if exclude_domain in exclude_list:
                        exclude_reason = f'excluded by -e {exclude_domain}'
                    else:
                        exclude_reason = f'excluded by EXCLUDE_DOMAINS from .env ({exclude_domain})'
                    break

        if domain == domain_item['name']:
            base_domain_found = True
            base_domain_description = domain_item.get('description', '')
            if not should_exclude:
                print(f'Processing base domain: {domain_item["name"]}')
                d = f.domain(domain_item['name'])
                extensions = d.extensions.list()
                total_extensions = len(extensions)
                # Filter excluded extensions
                filtered_extensions = filter_extensions(extensions, all_exclude_extensions)
                base_total_extensions = len(filtered_extensions)
                if total_extensions != base_total_extensions:
                    print(f'  Found {base_total_extensions} extension(s) (excluded {total_extensions - base_total_extensions} from count)')
                else:
                    print(f'  Found {base_total_extensions} extension(s)')
                base_domain_report.append(
                    f"<tr><td align='left'>{domain_item['name']}</td><td align='center'>{domain_item['description']}</td><td align='right'>{base_total_extensions}</td></tr>"
                )
            else:
                print(
                    f'Skipping base domain: {domain_item["name"]} ({exclude_reason or "excluded"})'
                )

        elif domain in domain_item['name']:
            if not should_exclude:
                print(f'Processing subdomain: {domain_item["name"]}')
                d = f.domain(domain_item['name'])
                extensions = d.extensions.list()
                total_extensions = len(extensions)
                # Filter excluded extensions
                filtered_extensions = filter_extensions(extensions, all_exclude_extensions)
                domain_total_extensions = len(filtered_extensions)
                if total_extensions != domain_total_extensions:
                    print(f'  Found {domain_total_extensions} extension(s) (excluded {total_extensions - domain_total_extensions} from count)')
                else:
                    print(f'  Found {domain_total_extensions} extension(s)')
                sub_total_domains += 1
                sub_total_extensions += domain_total_extensions
                sub_domains_report.append(
                    f"<tr><td align='center'>{domain_item['name']}</td><td align='center'>{domain_item['description']}</td><td align='right'>{domain_total_extensions}</td></tr>"
                )
            else:
                print(f'Skipping subdomain: {domain_item["name"]} ({exclude_reason})')

    # If base domain was found but row wasn't added, or if base domain wasn't found at all
    # Check if base domain row was already added by checking if report has only header rows (3 items)
    base_domain_row_added = len(base_domain_report) > 3

    if not base_domain_row_added:
        # Base domain row wasn't added - either not found, excluded, or had 0 extensions
        # Check if it should be excluded
        was_excluded = False
        if all_exclude_domains:
            for exclude_domain in all_exclude_domains:
                if exclude_domain in domain:
                    was_excluded = True
                    break

        if not was_excluded:
            # Try to process the base domain if it wasn't found in the list
            if not base_domain_found:
                # Base domain not in list, try to process it directly
                try:
                    print(f'Processing base domain (not in list): {domain}')
                    d = f.domain(domain)
                    extensions = d.extensions.list()
                    total_extensions = len(extensions)
                    # Filter excluded extensions
                    filtered_extensions = filter_extensions(extensions, all_exclude_extensions)
                    base_total_extensions = len(filtered_extensions)
                    if total_extensions != base_total_extensions:
                        print(f'  Found {base_total_extensions} extension(s) (excluded {total_extensions - base_total_extensions} from count)')
                    else:
                        print(f'  Found {base_total_extensions} extension(s)')
                    # Get description if available
                    for domain_item in domains:
                        if domain == domain_item['name']:
                            base_domain_description = domain_item.get('description', '')
                            break
                except Exception as e:
                    # If we can't process it, use defaults
                    print(f'  Warning: Could not process domain - {e}')
                    base_total_extensions = 0
                    base_domain_description = ''

            # Add the base domain row
            base_domain_report.append(
                f"<tr><td align='left'>{domain}</td><td align='center'>{base_domain_description}</td><td align='right'>{base_total_extensions}</td></tr>"
            )

    base_domain_report.append("<tr><th align='center' colspan='3'>Total</th></tr>")
    base_domain_report.append(
        f"<tr><th colspan='2'>1</th><th align='right'>{base_total_extensions}</th></tr>"
    )
    base_domain_report.append('</table>')
    base_domain_report.append('<p></p>')

    sub_domains_report.append("<tr><th align='center' colspan='3'>Total</th></tr>")
    sub_domains_report.append(
        f"<tr><td align='center' colspan='2'> {sub_total_domains}</td><td align='right'>{sub_total_extensions}</td></tr>"
    )
    sub_domains_report.append('</table>')

    # Print summary
    print('\n--- Summary ---')
    print(f'Base domain: {base_total_extensions} extension(s)')
    print(
        f'Subdomains: {sub_total_domains} domain(s) with {sub_total_extensions} extension(s)'
    )
    print(f'Total extensions: {base_total_extensions + sub_total_extensions}')
    print('')

    print('Generating customer_report.html')
    with open('customer_report.html', 'w') as file:
        file.write(header)
        file.write('\n'.join(base_domain_report))
        file.write('\n'.join(sub_domains_report))

    print('Converting customer_report.html to PDF')
    HTML('customer_report.html').write_pdf('customer_report.pdf')

    browser.quit()


if __name__ == '__main__':
    app()
