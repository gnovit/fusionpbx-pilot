from pilot.page_objects import Page
from pilot.page_objects.core import Domain, Domains


class FusionPBX():
    def __init__(self, browser, url, login_user, login_password):
        self.page = Page(browser, url, login_user, login_password)

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
        del (self.domain.name)
