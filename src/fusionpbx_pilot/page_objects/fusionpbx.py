from fusionpbx_pilot.page_objects import Page
from fusionpbx_pilot.page_objects.core import Domain, Domains


class FusionPBX:
    def __init__(self, browser, url, login_user, login_password):
        self.page = Page(browser, url, login_user, login_password)
        self.browser = browser

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    @property
    def domains(self):
        return Domains(self.page)

    @property
    def domain(self):
        return Domain(self.page)

    @domain.setter
    def domain(self, name):
        self.domain.name = name

    @domain.deleter
    def domain(self, name):
        self.domain.name = name
        del self.domain.name
