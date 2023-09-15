from pilot.page_objects import Page
from pilot.page_objects.core import Domain


class FusionPBX():
    def __init__(self, browser, url, login_user, login_password):
        self.page = Page(browser, url, login_user, login_password)

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
