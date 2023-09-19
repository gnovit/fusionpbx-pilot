from abc import ABC
from selenium.webdriver.common.by import By


app_path = "/core/domains/domains.php"
# app_edit_path = "/core/domains/domain_edit.php"


class DomainNotFound(Exception):
    def __init__(self, domain_name, message=None):
        if message is None:
            message = f"Extension {domain_name} not found"
        super().__init__(message)
        self.domain_name = domain_name


class Domains(ABC):
    """FusionPBX class to handle domains page"""

    def __init__(self, page):
        self.page = page

    def list(self):
        self.page.open(app_path)
        items = {
            "enabled": (By.CSS_SELECTOR, 'td button[title="Toggle"] span'),
            "description": (
                By.CSS_SELECTOR,
                'td[class="description overflow hide-sm-dn"]',
            ),
        }
        return self.page.container_rows(items)

    def toggle(self, domains: list):
        """Toggle domains Enabled/Disabled

        Args:
            domains (list): List of domains to toggle
        """

        self.page.open(app_path)
        self.page.select_rows(domains)

    def __repr__(self):
        return f"<Domains: {self.list()}>"
